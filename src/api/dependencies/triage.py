"""Triage service dependency initialization."""

import os

from langgraph.checkpoint.redis import RedisSaver

from src.modules.agents.translator.main import TranslatorAgent
from src.modules.agents.supervisor.main import SupervisorAgent
from src.modules.agents.specialists.billing.main import BillingAgent
from src.modules.agents.specialists.technical.main import TechnicalAgent
from src.modules.agents.specialists.general.main import GeneralAgent
from src.modules.agents.ticket_matcher.main import TicketMatcherAgent
from src.modules.agents.specialists.tools.kb_retrieval import KBRetrievalTool
from src.modules.agents.supervisor.tools.customer_lookup import CustomerLookupTool
from src.modules.agents.ticket_matcher.tools.ticket_summarize import TicketSummarizeTool
from src.modules.graph.workflow import MultiAgentWorkflow
from src.repositories.checkpoint.main import CheckpointRepository
from src.repositories.ticket.main import TicketRepository
from src.repositories.chat.main import ChatRepository
from src.usecases.triage.main import TriageService
from libs.database.tabular.sql.selector import SQLClientSelector
from libs.database.keyvalue_db.selector import KeyValueClientSelector
from libs.llm.client.selector import LLMClientSelector
from libs.llm.observability.selector import ObservabilitySelector
from libs.llm.prompt_manager.selector import PromptManagerSelector
from libs.database.vector.selector import VectorStoreSelector
from libs.configs.base import BaseConfigManager
from libs.logger.logger import get_logger

logger = get_logger(__name__)


def initialize_services(
    settings: BaseConfigManager,
) -> tuple[TriageService, RedisSaver]:
    """Initialize and return the triage service.

    Creates:
    - Repositories: CheckpointRepository, TicketRepository, ChatRepository
    - Workflow: MultiAgentWorkflow (translator → supervisor → specialists)
    - Services: TriageService

    Args:
        settings: Application configuration manager.

    Returns:
        Tuple of (TriageService, RedisSaver checkpointer).
    """

    logger.info("Initializing LLM clients...")
    proxy_url = settings.agent_shared.llm.proxy_url
    api_key = settings.agent_shared.llm.api_key

    # LangChain client for agents (has bind_tools for create_agent)
    langchain_client = LLMClientSelector.create(
        provider="langchain",
        proxy_url=proxy_url,
        api_key=api_key,
        default_model=settings.triage.llm.model,
    )
    llm = langchain_client.get_client(model=settings.triage.llm.model)

    # LiteLLM client for embeddings
    embedding_client = LLMClientSelector.create(
        provider="litellm",
        proxy_url=proxy_url,
        api_key=api_key,
        embedding_model=settings.triage.llm.embedding_model,
    )

    logger.info("Initializing vector store...")
    vector_store = VectorStoreSelector.create(
        provider=settings.agent_shared.vectordb.provider,
        host=settings.agent_shared.vectordb.host,
        port=int(settings.agent_shared.vectordb.port),
        collection_name=settings.triage.vectordb.collection_name,
        vector_size=int(settings.agent_shared.vectordb.vector_size),
    )

    logger.info("Initializing observability (Langfuse)...")
    observability = ObservabilitySelector.create(provider="langfuse")

    logger.info("Initializing prompt manager (Langfuse)...")
    prompt_manager = PromptManagerSelector.create(provider="langfuse")

    logger.info("Initializing Redis client...")
    redis_host = os.getenv("REDIS_HOST", "redis")
    redis_port = int(os.getenv("REDIS_PORT", "6379"))
    kv_client = KeyValueClientSelector.create(
        provider="redis",
        host=redis_host,
        port=redis_port,
        decode_responses=True,
    )
    # LangGraph RedisSaver needs raw redis.Redis client
    checkpointer = RedisSaver(redis_client=kv_client.get_raw_client())
    checkpointer.setup()

    logger.info("Initializing PostgreSQL client...")
    postgres_host = os.getenv("POSTGRES_HOST", "postgres")
    postgres_port = os.getenv("POSTGRES_PORT", "5432")
    postgres_db = os.getenv("POSTGRES_DB", "support_triage")
    postgres_user = os.getenv("POSTGRES_USER", "postgres")
    postgres_password = os.getenv("POSTGRES_PASSWORD", "postgres")

    sql_client = SQLClientSelector.create(
        provider="postgres",
        host=postgres_host,
        port=int(postgres_port),
        database=postgres_db,
        user=postgres_user,
        password=postgres_password,
    )

    # === Create Repositories ===
    logger.info("Creating repositories...")
    checkpoint_repo = CheckpointRepository(
        checkpointer=checkpointer,
        kv_client=kv_client,
    )
    ticket_repo = TicketRepository(db_client=sql_client)
    chat_repo = ChatRepository(db_client=sql_client)

    # === Create Agents ===
    agent_configs = settings.triage.agents

    # TranslatorAgent (no tools)
    logger.info("Creating TranslatorAgent...")
    translator_agent = TranslatorAgent(
        llm=llm,
        observability=observability,
        prompt_manager=prompt_manager,
        agent_config=agent_configs.translator,
    )

    # SupervisorAgent with customer_lookup tool
    logger.info("Creating SupervisorAgent...")
    customer_tool = CustomerLookupTool(db_client=sql_client)
    supervisor_agent = SupervisorAgent(
        llm=llm,
        tools=[customer_tool],
        observability=observability,
        prompt_manager=prompt_manager,
        agent_config=agent_configs.supervisor,
    )

    # BillingAgent with kb_search (billing category)
    logger.info("Creating BillingAgent...")
    billing_kb_tool = KBRetrievalTool(
        vector_store=vector_store,
        llm=embedding_client,
        category_filter=agent_configs.billing.get("category_filter", "billing"),
    )
    billing_agent = BillingAgent(
        llm=llm,
        tools=[billing_kb_tool],
        observability=observability,
        prompt_manager=prompt_manager,
        agent_config=agent_configs.billing,
    )

    # TechnicalAgent with kb_search (technical category)
    logger.info("Creating TechnicalAgent...")
    technical_kb_tool = KBRetrievalTool(
        vector_store=vector_store,
        llm=embedding_client,
        category_filter=agent_configs.technical.get("category_filter", "technical"),
    )
    technical_agent = TechnicalAgent(
        llm=llm,
        tools=[technical_kb_tool],
        observability=observability,
        prompt_manager=prompt_manager,
        agent_config=agent_configs.technical,
    )

    # GeneralAgent with kb_search (general category)
    logger.info("Creating GeneralAgent...")
    general_kb_tool = KBRetrievalTool(
        vector_store=vector_store,
        llm=embedding_client,
        category_filter=agent_configs.general.get("category_filter", "general"),
    )
    general_agent = GeneralAgent(
        llm=llm,
        tools=[general_kb_tool],
        observability=observability,
        prompt_manager=prompt_manager,
        agent_config=agent_configs.general,
    )

    # TicketMatcherAgent (used by TriageService for pre-workflow matching)
    logger.info("Creating TicketMatcherAgent...")
    ticket_matcher_agent = TicketMatcherAgent(
        llm=llm,
        observability=observability,
        prompt_manager=prompt_manager,
        agent_config=agent_configs.get("ticket_matcher", {}),
    )

    # TicketSummarizeTool (used by TriageService for summarizing activated tickets)
    logger.info("Creating TicketSummarizeTool...")
    ticket_summarize_tool = TicketSummarizeTool(kv_client=kv_client)

    # === Create Workflow ===
    logger.info("Creating MultiAgentWorkflow...")
    workflow = MultiAgentWorkflow(
        translator_agent=translator_agent,
        supervisor_agent=supervisor_agent,
        billing_agent=billing_agent,
        technical_agent=technical_agent,
        general_agent=general_agent,
        observability=observability,
        checkpointer=checkpointer,
    )

    # === Create Services ===
    logger.info("Creating TriageService...")
    triage_service = TriageService(
        workflow=workflow,
        checkpoint_repo=checkpoint_repo,
        ticket_repo=ticket_repo,
        chat_repo=chat_repo,
        ticket_matcher_agent=ticket_matcher_agent,
        ticket_summarize_tool=ticket_summarize_tool,
    )

    logger.info("Service initialization complete")
    return triage_service, checkpointer

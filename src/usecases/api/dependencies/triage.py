"""Multi-agent triage workflow dependency initialization."""

import os

import redis
from langgraph.checkpoint.redis import RedisSaver

from src.modules.agents.translator import TranslatorAgent
from src.modules.agents.supervisor import SupervisorAgent
from src.modules.agents.billing import BillingAgent
from src.modules.agents.technical import TechnicalAgent
from src.modules.agents.general import GeneralAgent
from src.modules.agents.tools.kb_retrieval import KBRetrievalTool
from src.modules.agents.tools.customer_lookup import CustomerLookupTool
from src.modules.graph.workflow import MultiAgentWorkflow
from libs.llm.client.selector import LLMClientSelector
from libs.llm.observability.selector import ObservabilitySelector
from libs.llm.prompt_manager.selector import PromptManagerSelector
from libs.database.vector.selector import VectorStoreSelector
from libs.configs.base import BaseConfigManager
from libs.logger.logger import get_logger

logger = get_logger(__name__)


def initialize_triage_workflow(settings: BaseConfigManager) -> MultiAgentWorkflow:
    """Initialize and return the multi-agent triage workflow with all dependencies.

    Creates:
    - TranslatorAgent: Language detection and translation
    - SupervisorAgent: Classification and routing with customer_lookup tool
    - BillingAgent: Billing specialist with kb_search (billing category)
    - TechnicalAgent: Technical specialist with kb_search (technical category)
    - GeneralAgent: General specialist with kb_search (general category)

    Args:
        settings: Application configuration manager.

    Returns:
        Configured MultiAgentWorkflow instance.
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
    )

    logger.info("Initializing observability (Langfuse)...")
    observability = ObservabilitySelector.create(provider="langfuse")

    logger.info("Initializing prompt manager (Langfuse)...")
    prompt_manager = PromptManagerSelector.create(provider="langfuse")

    logger.info("Initializing Redis checkpointer...")
    redis_host = os.getenv("REDIS_HOST", "redis")
    redis_port = int(os.getenv("REDIS_PORT", "6379"))
    redis_client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
    checkpointer = RedisSaver(redis_client=redis_client)
    checkpointer.setup()

    # Get agent configs
    agent_configs = settings.triage.agents

    # Initialize TranslatorAgent (no tools)
    logger.info("Creating TranslatorAgent...")
    translator_agent = TranslatorAgent(
        llm=llm,
        observability=observability,
        prompt_manager=prompt_manager,
        agent_config=agent_configs.translator,
    )

    # Initialize SupervisorAgent with customer_lookup tool
    logger.info("Creating SupervisorAgent...")
    customer_tool = CustomerLookupTool(data_path="data/customers.json")
    supervisor_agent = SupervisorAgent(
        llm=llm,
        tools=[customer_tool],
        observability=observability,
        prompt_manager=prompt_manager,
        agent_config=agent_configs.supervisor,
    )

    # Initialize BillingAgent with kb_search (billing category)
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

    # Initialize TechnicalAgent with kb_search (technical category)
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

    # Initialize GeneralAgent with kb_search (general category)
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

    # Create multi-agent workflow
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

    logger.info("Multi-agent triage workflow initialization complete")
    return workflow

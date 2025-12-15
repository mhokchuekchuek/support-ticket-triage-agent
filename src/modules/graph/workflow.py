"""Multi-agent workflow for ticket triage using LangGraph."""

from typing import Optional

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.base import BaseCheckpointSaver

from src.modules.graph.state import AgentState, create_initial_state
from src.modules.agents.base import BaseAgent
from src.entities.ticket import Ticket
from src.entities.triage_result import (
    TriageResult,
    UrgencyLevel,
    RecommendedAction,
    ExtractedInfo,
)
from libs.llm.observability.base import BaseObservability
from libs.logger.logger import get_logger

logger = get_logger(__name__)


class MultiAgentWorkflow:
    """LangGraph workflow for multi-agent ticket triage.

    Simplified workflow - agent execution only.
    Pre/post workflow logic (ticket matching, persistence) handled by TriageService.

    Flow:
    START → translator → supervisor → [billing|technical|general|escalate] → END

    Attributes:
        translator_agent: Agent for language detection and translation.
        supervisor_agent: Agent for classification and routing.
        billing_agent: Specialist for billing issues.
        technical_agent: Specialist for technical issues.
        general_agent: Specialist for general inquiries.
        observability: Observability client for tracing.
        checkpointer: Checkpointer for state persistence.
        graph: Compiled LangGraph state graph.
    """

    def __init__(
        self,
        translator_agent: BaseAgent,
        supervisor_agent: BaseAgent,
        billing_agent: BaseAgent,
        technical_agent: BaseAgent,
        general_agent: BaseAgent,
        observability: Optional[BaseObservability] = None,
        checkpointer: Optional[BaseCheckpointSaver] = None,
    ):
        """Initialize the multi-agent workflow.

        Args:
            translator_agent: Agent for language detection/translation.
            supervisor_agent: Agent for classification and routing.
            billing_agent: Specialist agent for billing issues.
            technical_agent: Specialist agent for technical issues.
            general_agent: Specialist agent for general inquiries.
            observability: Observability client for Langfuse tracing.
            checkpointer: LangGraph checkpointer for state persistence.
        """
        self.translator_agent = translator_agent
        self.supervisor_agent = supervisor_agent
        self.billing_agent = billing_agent
        self.technical_agent = technical_agent
        self.general_agent = general_agent
        self.observability = observability
        self.checkpointer = checkpointer
        self.graph = self._build_graph()

    def _build_graph(self) -> StateGraph:
        """Build the LangGraph state graph.

        Flow: START → translator → supervisor → [billing|technical|general|escalate] → END

        Returns:
            Compiled StateGraph for the workflow.
        """
        graph = StateGraph(AgentState)

        # Add nodes for each agent
        graph.add_node("translator", self.translator_agent.execute)
        graph.add_node("supervisor", self.supervisor_agent.execute)
        graph.add_node("billing", self.billing_agent.execute)
        graph.add_node("technical", self.technical_agent.execute)
        graph.add_node("general", self.general_agent.execute)
        graph.add_node("escalate", self._create_escalation_result)

        # Set entry point
        graph.set_entry_point("translator")

        # Translator → Supervisor
        graph.add_edge("translator", "supervisor")

        # Supervisor routes to specialists
        graph.add_conditional_edges(
            "supervisor",
            self._route_from_supervisor,
            {
                "billing": "billing",
                "technical": "technical",
                "general": "general",
                "escalate": "escalate",
            },
        )

        # All specialists go to END
        graph.add_edge("billing", END)
        graph.add_edge("technical", END)
        graph.add_edge("general", END)
        graph.add_edge("escalate", END)

        return graph.compile(checkpointer=self.checkpointer)

    def _route_from_supervisor(self, state: AgentState) -> str:
        """Route based on supervisor's decision.

        Args:
            state: Current agent state with supervisor decision.

        Returns:
            Node name to route to.
        """
        decision = state.get("supervisor_decision")

        if not decision:
            logger.warning("No supervisor decision, routing to general")
            return "general"

        # Direct escalation for critical cases
        if decision.requires_escalation:
            logger.info("Direct escalation requested by supervisor")
            return "escalate"

        # Route to specialist based on ticket type
        return decision.ticket_type.value

    def _create_escalation_result(self, state: AgentState) -> AgentState:
        """Create triage result for direct escalation.

        Args:
            state: Current agent state.

        Returns:
            Updated state with escalation triage result.
        """
        ticket = state["ticket"]
        decision = state.get("supervisor_decision")
        translation = state.get("translation")

        logger.info(f"Creating escalation result for ticket: {ticket.ticket_id}")

        urgency = decision.urgency if decision else UrgencyLevel.HIGH
        language = translation.original_language if translation else "en"

        state["triage_result"] = TriageResult(
            urgency=urgency,
            extracted_info=ExtractedInfo(
                product_area=decision.ticket_type.value if decision else "general",
                issue_type="escalation",
                sentiment="urgent",
                language=language,
            ),
            recommended_action=RecommendedAction.ESCALATE_HUMAN,
            reasoning=decision.reasoning if decision else "Direct escalation required",
        )

        state["current_agent"] = "escalate"

        return state

    def invoke(
        self,
        ticket: Ticket,
        config: Optional[dict] = None,
    ) -> AgentState:
        """Run the multi-agent triage workflow on a ticket.

        Pre/post workflow logic handled by TriageService.
        This method only runs the agent graph.

        Args:
            ticket: Support ticket to triage.
            config: LangGraph config (should include thread_id from TriageService).

        Returns:
            Final AgentState with triage result.
        """
        customer_id = ticket.customer_id

        logger.info(f"Starting agent workflow for ticket: {ticket.ticket_id}")

        run_config = config or {}

        # Add observability callbacks
        if self.observability:
            callback_handler = self.observability.get_callback_handler(
                session_id=customer_id,
                user_id=customer_id,
                metadata={
                    "ticket_id": ticket.ticket_id,
                    "plan": ticket.customer_info.plan if ticket.customer_info else None,
                    "region": ticket.customer_info.region if ticket.customer_info else None,
                },
            )
            if callback_handler:
                run_config["callbacks"] = run_config.get("callbacks", []) + [
                    callback_handler
                ]
                run_config["metadata"] = {
                    "langfuse_session_id": customer_id,
                    "langfuse_user_id": customer_id,
                }

        # Create initial state and run workflow
        initial_state = create_initial_state(ticket)
        result = self.graph.invoke(initial_state, config=run_config)

        # Flush observability traces
        if self.observability:
            self.observability.flush()

        logger.info(f"Agent workflow complete for ticket: {ticket.ticket_id}")
        return result

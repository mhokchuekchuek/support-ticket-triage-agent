"""Triage use case - application business logic."""

import uuid
from typing import Optional, Any

from langchain.tools import BaseTool

from src.modules.graph.workflow import MultiAgentWorkflow
from src.modules.agents.base import BaseAgent
from src.repositories.checkpoint.main import CheckpointRepository
from src.repositories.ticket.main import TicketRepository
from src.repositories.chat.main import ChatRepository
from src.entities.ticket import Ticket
from src.entities.triage_result import RecommendedAction
from libs.logger.logger import get_logger

logger = get_logger(__name__)


class TriageService:
    """Use case for ticket triage operations.

    Handles:
    - Pre-workflow: scan activated tickets, summarize, match
    - Workflow execution: agent graph only
    - Post-workflow: persist completed tickets or keep activated

    Terminology:
    - Activated ticket: In-progress, waiting in Redis
    - Completed ticket: Resolved/escalated, stored in PostgreSQL

    Attributes:
        _workflow: Multi-agent workflow for agent execution.
        _checkpoint_repo: Repository for checkpoint/Redis operations.
        _ticket_repo: Repository for ticket SQL operations.
        _chat_repo: Repository for chat message SQL operations.
        _ticket_matcher_agent: Agent for matching messages to activated tickets.
        _ticket_summarize_tool: Tool for summarizing activated tickets.
    """

    def __init__(
        self,
        workflow: MultiAgentWorkflow,
        checkpoint_repo: CheckpointRepository,
        ticket_repo: TicketRepository,
        chat_repo: ChatRepository,
        ticket_matcher_agent: Optional[BaseAgent] = None,
        ticket_summarize_tool: Optional[BaseTool] = None,
    ):
        """Initialize triage service.

        Args:
            workflow: Multi-agent workflow for agent execution.
            checkpoint_repo: Repository for checkpoint/Redis operations.
            ticket_repo: Repository for ticket SQL operations.
            chat_repo: Repository for chat message SQL operations.
            ticket_matcher_agent: Optional agent for ticket matching.
            ticket_summarize_tool: Optional tool for ticket summarization.
        """
        self._workflow = workflow
        self._checkpoint_repo = checkpoint_repo
        self._ticket_repo = ticket_repo
        self._chat_repo = chat_repo
        self._ticket_matcher_agent = ticket_matcher_agent
        self._ticket_summarize_tool = ticket_summarize_tool
        logger.info("TriageService initialized")

    def triage_ticket(
        self,
        ticket: Ticket,
        config: Optional[dict[str, Any]] = None,
    ) -> dict:
        """Execute full triage flow on a ticket.

        Flow:
        1. Pre-workflow: Check for activated tickets, match if found
        2. Workflow: Run agent graph (translator → supervisor → specialist)
        3. Post-workflow: Persist or keep activated based on result

        Args:
            ticket: Ticket to triage.
            config: Optional workflow configuration.

        Returns:
            Workflow result containing triage decision.
        """
        customer_id = ticket.customer_id
        new_message = ticket.messages[-1].content if ticket.messages else ""

        logger.info(f"Starting triage for customer: {customer_id}")

        # === PRE-WORKFLOW: Ticket matching ===
        final_ticket_id = self._resolve_ticket_id(ticket, customer_id, new_message)
        ticket.ticket_id = final_ticket_id

        # === WORKFLOW: Agent execution ===
        run_config = self._build_config(config, customer_id, final_ticket_id)
        result = self._workflow.invoke(ticket, run_config)

        # === POST-WORKFLOW: Persist or keep activated ===
        self._handle_persistence(result, ticket)

        logger.info(f"Triage complete for ticket: {final_ticket_id}")
        return result

    def _resolve_ticket_id(
        self,
        ticket: Ticket,
        customer_id: str,
        new_message: str,
    ) -> str:
        """Resolve ticket ID: match to activated ticket or generate new.

        Args:
            ticket: Ticket being processed.
            customer_id: Customer identifier.
            new_message: Latest message content.

        Returns:
            Resolved ticket ID.
        """
        if self._ticket_matcher_agent:
            activated_ids = self._checkpoint_repo.scan_activated_ticket_ids(customer_id)
            logger.info(f"Found {len(activated_ids)} activated tickets for customer")

            if activated_ids:
                summaries = self._get_ticket_summaries(customer_id, activated_ids)
                matched_id = self._match_ticket(new_message, summaries)
                if matched_id:
                    logger.info(f"Matched to activated ticket: {matched_id}")
                    return matched_id

        # No match - use provided ID or generate new
        if ticket.ticket_id:
            return ticket.ticket_id

        new_id = self._generate_ticket_id()
        logger.info(f"Generated new ticket ID: {new_id}")
        return new_id

    def _get_ticket_summaries(
        self,
        customer_id: str,
        ticket_ids: list[str],
    ) -> list[dict]:
        """Get summaries for activated tickets.

        Args:
            customer_id: Customer identifier.
            ticket_ids: List of activated ticket IDs.

        Returns:
            List of ticket summaries.
        """
        if not self._ticket_summarize_tool:
            return []

        summaries = []
        for ticket_id in ticket_ids:
            try:
                summary = self._ticket_summarize_tool._run(
                    ticket_id=ticket_id,
                    customer_id=customer_id,
                )
                summaries.append({"ticket_id": ticket_id, "summary": summary})
            except Exception as e:
                logger.warning(f"Failed to summarize ticket {ticket_id}: {e}")

        return summaries

    def _match_ticket(
        self,
        new_message: str,
        activated_tickets: list[dict],
    ) -> Optional[str]:
        """Match new message to activated ticket.

        Args:
            new_message: New message content.
            activated_tickets: List of activated ticket summaries.

        Returns:
            Matched ticket ID or None.
        """
        if not self._ticket_matcher_agent or not activated_tickets:
            return None

        state = {
            "new_message": new_message,
            "activated_tickets": activated_tickets,
        }
        result = self._ticket_matcher_agent.execute(state)
        match_result = result.get("match_result", {})

        confidence = match_result.get("confidence", "low")
        if confidence in ("high", "medium"):
            return match_result.get("matched_ticket_id")

        return None

    def _build_config(
        self,
        config: Optional[dict],
        customer_id: str,
        ticket_id: str,
    ) -> dict:
        """Build workflow config with thread_id for checkpointing.

        Args:
            config: Optional base configuration.
            customer_id: Customer identifier.
            ticket_id: Ticket identifier.

        Returns:
            Configuration dict with thread_id set.
        """
        run_config = config or {}
        run_config["configurable"] = run_config.get("configurable", {})
        run_config["configurable"]["thread_id"] = f"{customer_id}:{ticket_id}"
        return run_config

    def _handle_persistence(self, result: dict, ticket: Ticket) -> None:
        """Persist completed ticket or keep as activated.

        Args:
            result: Workflow result.
            ticket: Ticket being processed.
        """
        triage_result = result.get("triage_result")
        if not triage_result:
            logger.warning("No triage result, skipping persistence")
            return

        action = triage_result.recommended_action

        if action in (RecommendedAction.AUTO_RESPOND, RecommendedAction.ESCALATE_HUMAN):
            logger.info(f"Ticket completed ({action.value}), persisting to PostgreSQL")
            self._persist_ticket(result, ticket)
        else:
            logger.info(f"Ticket needs continuation ({action.value}), keeping activated in Redis")

    def _persist_ticket(self, result: dict, ticket: Ticket) -> None:
        """Save ticket to PostgreSQL and cleanup Redis.

        Args:
            result: Workflow result.
            ticket: Ticket to persist.
        """
        triage_result = result.get("triage_result")
        messages = result.get("messages", [])

        # Save ticket record
        self._ticket_repo.save_ticket(
            ticket_id=ticket.ticket_id,
            customer_id=ticket.customer_id,
            status="closed",
            urgency=triage_result.urgency.value,
            ticket_type=triage_result.extracted_info.product_area,
            triage_result=triage_result.model_dump() if hasattr(triage_result, "model_dump") else {},
        )
        logger.info(f"Saved ticket record: {ticket.ticket_id}")

        # Save chat messages
        msg_dicts = []
        for msg in messages:
            role = "human" if hasattr(msg, "type") and msg.type == "human" else "ai"
            msg_dicts.append({"role": role, "content": msg.content})

        if msg_dicts:
            self._chat_repo.save_messages(ticket.ticket_id, ticket.customer_id, msg_dicts)
            logger.info(f"Saved {len(msg_dicts)} messages for ticket: {ticket.ticket_id}")

        # Cleanup Redis checkpoints
        deleted = self._checkpoint_repo.delete_ticket_checkpoints(
            ticket.customer_id, ticket.ticket_id
        )
        logger.info(f"Deleted {deleted} Redis keys for ticket: {ticket.ticket_id}")

    def _generate_ticket_id(self) -> str:
        """Generate new ticket ID.

        Returns:
            New ticket ID in format TKT-XXXXXXXX.
        """
        return f"TKT-{uuid.uuid4().hex[:8].upper()}"

"""Workflow validator for triage evaluation scenarios.

Validates that correct agents and tools were used based on scenario expectations
by analyzing Langfuse traces.
"""

import time
from typing import Any, Dict, List, Optional

from langfuse import Langfuse

from evaluation.scenarios.base import TriageScenario, WorkflowExpectation
from libs.logger.logger import get_logger

logger = get_logger(__name__)


class WorkflowValidator:
    """Validates agent and tool selection against scenario expectations.

    Uses Langfuse traces to verify:
    - Correct agents were invoked (translator, supervisor, specialists)
    - Correct tools were called (customer_lookup, kb_search)
    - Excluded agents/tools were not used

    Example:
        >>> validator = WorkflowValidator(langfuse_client)
        >>> result = validator.validate(scenario, "eval-billing-01-20241115")
        >>> print(result['pass'])  # True or False
        >>> print(result['agents']['missing'])  # ['billing'] if missing
    """

    # Agent name mappings (observation names in traces)
    AGENT_NAMES = {
        "translator": ["TranslatorAgent", "translator", "Translator"],
        "supervisor": ["SupervisorAgent", "supervisor", "Supervisor"],
        "billing": ["BillingAgent", "billing", "Billing"],
        "technical": ["TechnicalAgent", "technical", "Technical"],
        "general": ["GeneralAgent", "general", "General"],
        "escalate": ["escalate", "escalation", "Escalation"],
    }

    # Tool name mappings
    TOOL_NAMES = {
        "customer_lookup": ["customer_lookup", "CustomerLookup", "CustomerLookupTool"],
        "kb_search": ["kb_search", "KBRetrievalTool", "kb_retrieval", "KBSearch"],
    }

    def __init__(self, langfuse_client: Optional[Langfuse] = None):
        """Initialize workflow validator.

        Args:
            langfuse_client: Langfuse client for fetching traces
        """
        self.langfuse_client = langfuse_client
        logger.info("WorkflowValidator initialized")

    def validate(
        self,
        scenario: TriageScenario,
        session_id: str,
    ) -> Dict[str, Any]:
        """Validate workflow against scenario expectations.

        Fetches the Langfuse trace for the given session and validates
        that the expected agents and tools were used.

        Args:
            scenario: Scenario with expected_workflow
            session_id: Session ID to fetch trace (ticket_id)

        Returns:
            Validation results with pass/fail and details:
            {
                'pass': True/False,
                'agents': {'pass': bool, 'expected': [...], 'missing': [...]},
                'tools': {'pass': bool, 'expected': [...], 'missing': [...]},
                'agents_used': [...],
                'tools_used': [...]
            }
        """
        logger.info(f"Validating workflow for session: {session_id}")

        try:
            # Fetch trace from Langfuse
            trace_data = self._fetch_trace(session_id)
            if not trace_data:
                return {
                    "pass": False,
                    "error": "Could not fetch trace from Langfuse",
                    "agents": {},
                    "tools": {},
                }

            # Extract agents and tools used
            agents_used = self._extract_agents(trace_data)
            tools_used = self._extract_tools(trace_data)

            logger.debug(f"Agents used: {agents_used}")
            logger.debug(f"Tools used: {tools_used}")

            # Validate against expectations
            expected = scenario.expected_workflow

            agents_validation = self._validate_agents(agents_used, expected)
            tools_validation = self._validate_tools(tools_used, expected)

            # Overall pass if both pass
            overall_pass = agents_validation["pass"] and tools_validation["pass"]

            return {
                "pass": overall_pass,
                "agents": agents_validation,
                "tools": tools_validation,
                "agents_used": agents_used,
                "tools_used": tools_used,
            }

        except Exception as e:
            logger.error(f"Workflow validation failed: {e}", exc_info=True)
            return {
                "pass": False,
                "error": str(e),
                "agents": {},
                "tools": {},
            }

    def _fetch_trace(
        self,
        session_id: str,
        max_retries: int = 10,
        retry_delay: int = 3,
    ) -> Optional[Dict[str, Any]]:
        """Fetch trace from Langfuse by session_id with retry logic.

        Langfuse traces are submitted asynchronously, so we need to
        retry a few times to allow for propagation.

        Args:
            session_id: Session ID (ticket_id used as session)
            max_retries: Maximum retry attempts
            retry_delay: Seconds between retries

        Returns:
            Trace data dict with 'trace' and 'observations', or None if not found
        """
        if not self.langfuse_client:
            logger.warning("Langfuse client not available, skipping trace fetch")
            return None

        for attempt in range(max_retries):
            try:
                # Fetch traces filtered by session_id
                traces_response = self.langfuse_client.api.trace.list(
                    limit=1,
                    session_id=session_id,
                )

                if (
                    traces_response
                    and hasattr(traces_response, "data")
                    and len(traces_response.data) > 0
                ):
                    trace = traces_response.data[0]
                    logger.info(f"Fetched trace on attempt {attempt + 1}: {trace.id}")

                    # Fetch observations for the trace
                    observations_response = self.langfuse_client.api.observations.get_many(
                        trace_id=trace.id,
                        limit=100,
                    )

                    return {
                        "trace": trace,
                        "observations": (
                            observations_response.data if observations_response else []
                        ),
                    }

                if attempt < max_retries - 1:
                    logger.debug(
                        f"Trace not found (attempt {attempt + 1}/{max_retries}), "
                        f"retrying in {retry_delay}s..."
                    )
                    time.sleep(retry_delay)

            except Exception as e:
                logger.warning(f"Error fetching trace (attempt {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)

        logger.warning(f"No trace found for session_id: {session_id}")
        return None

    def _extract_agents(self, trace_data: Dict[str, Any]) -> List[str]:
        """Extract agent names from trace observations.

        Parses Langfuse observations to identify which agents were
        invoked during the triage workflow.

        Args:
            trace_data: Trace data with observations

        Returns:
            List of normalized agent names used (e.g., ["translator", "supervisor", "billing"])
        """
        agents = set()
        observations = trace_data.get("observations", [])

        for obs in observations:
            obs_name = getattr(obs, "name", "")
            obs_type = getattr(obs, "type", "")

            # Check against known agent names
            for agent_key, agent_variants in self.AGENT_NAMES.items():
                if obs_name in agent_variants or any(
                    v.lower() in obs_name.lower() for v in agent_variants
                ):
                    agents.add(agent_key)
                    break

            # Also check metadata for agent identification
            if hasattr(obs, "metadata") and obs.metadata:
                metadata = obs.metadata
                if isinstance(metadata, dict):
                    agent_name = metadata.get("agent_name", "")
                    for agent_key, agent_variants in self.AGENT_NAMES.items():
                        if agent_name in agent_variants or any(
                            v.lower() in agent_name.lower() for v in agent_variants
                        ):
                            agents.add(agent_key)
                            break

        return sorted(list(agents))

    def _extract_tools(self, trace_data: Dict[str, Any]) -> List[str]:
        """Extract tool names from trace observations.

        Parses Langfuse observations to identify which tools were
        called during the triage workflow.

        Args:
            trace_data: Trace data with observations

        Returns:
            List of normalized tool names used (e.g., ["customer_lookup", "kb_search"])
        """
        tools = set()
        observations = trace_data.get("observations", [])

        logger.debug(f"Extracting tools from {len(observations)} observations")

        for obs in observations:
            obs_name = getattr(obs, "name", "")
            obs_type = getattr(obs, "type", "")

            # Check against known tool names
            for tool_key, tool_variants in self.TOOL_NAMES.items():
                if obs_name in tool_variants or any(
                    v.lower() in obs_name.lower() for v in tool_variants
                ):
                    tools.add(tool_key)
                    logger.debug(f"Found tool: {tool_key} (from {obs_name})")
                    break

            # Check metadata for tool calls
            if hasattr(obs, "metadata") and obs.metadata:
                metadata = obs.metadata
                if isinstance(metadata, dict):
                    tool_name = metadata.get("tool_name", "")
                    for tool_key, tool_variants in self.TOOL_NAMES.items():
                        if tool_name in tool_variants or any(
                            v.lower() in tool_name.lower() for v in tool_variants
                        ):
                            tools.add(tool_key)
                            logger.debug(f"Found tool in metadata: {tool_key}")
                            break

                    # Check for tools_used array in metadata
                    tools_used_meta = metadata.get("tools_used", [])
                    if isinstance(tools_used_meta, list):
                        for tool in tools_used_meta:
                            for tool_key, tool_variants in self.TOOL_NAMES.items():
                                if tool in tool_variants:
                                    tools.add(tool_key)
                                    break

        return sorted(list(tools))

    def _validate_agents(
        self,
        agents_used: List[str],
        expected: WorkflowExpectation,
    ) -> Dict[str, Any]:
        """Validate agents against expectations.

        Checks that all expected agents were used and no excluded
        agents were invoked.

        Args:
            agents_used: List of agents that were used
            expected: WorkflowExpectation object

        Returns:
            Validation result dict with pass/fail and details
        """
        agents_set = set(agents_used)
        should_include = set(expected.agents_should_include)
        should_exclude = set(expected.agents_should_exclude)

        # Check inclusions (expected agents that are missing)
        missing = should_include - agents_set
        # Check exclusions (excluded agents that were used)
        unwanted = agents_set & should_exclude

        passed = len(missing) == 0 and len(unwanted) == 0

        return {
            "pass": passed,
            "expected": expected.agents_should_include,
            "excluded": expected.agents_should_exclude,
            "actual": agents_used,
            "missing": sorted(list(missing)),
            "unwanted": sorted(list(unwanted)),
        }

    def _validate_tools(
        self,
        tools_used: List[str],
        expected: WorkflowExpectation,
    ) -> Dict[str, Any]:
        """Validate tools against expectations.

        Checks that all expected tools were called and no excluded
        tools were invoked.

        Args:
            tools_used: List of tools that were used
            expected: WorkflowExpectation object

        Returns:
            Validation result dict with pass/fail and details
        """
        tools_set = set(tools_used)
        should_include = set(expected.tools_should_include)
        should_exclude = set(expected.tools_should_exclude)

        # Check inclusions (expected tools that are missing)
        missing = should_include - tools_set
        # Check exclusions (excluded tools that were used)
        unwanted = tools_set & should_exclude

        passed = len(missing) == 0 and len(unwanted) == 0

        return {
            "pass": passed,
            "expected": expected.tools_should_include,
            "excluded": expected.tools_should_exclude,
            "actual": tools_used,
            "missing": sorted(list(missing)),
            "unwanted": sorted(list(unwanted)),
        }

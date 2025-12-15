"""Evaluation runner for triage agent responses.

Runs scenarios through the triage API and evaluates quality with LLM-as-a-Judge.
Integrated with Langfuse for score tracking and workflow validation.
"""

import time
from datetime import datetime
from typing import Any, Dict, List, Optional

import requests
from langfuse import Langfuse

from evaluation.config import get_evaluation_config
from evaluation.llm_judge import LLMJudge
from evaluation.workflow_validator import WorkflowValidator
from evaluation.scenarios import (
    billing,
    technical,
    general,
    escalation,
    multilingual,
    edge_cases,
)
from evaluation.scenarios.base import TriageScenario
from libs.logger.logger import get_logger

logger = get_logger(__name__)


class TriageEvaluator:
    """Evaluation runner for triage agent workflow quality assessment.

    Orchestrates:
    1. Running scenarios through the triage API
    2. Validating workflow execution via Langfuse traces
    3. Evaluating triage quality with LLM-as-a-Judge
    4. Logging scores to Langfuse for tracking

    Example:
        >>> evaluator = TriageEvaluator()
        >>> results = evaluator.run_all_scenarios()
        >>> for r in results:
        ...     print(f"{r['scenario']}: {r['classification']['urgency_accuracy']}")
    """

    def __init__(self, config: Optional[Any] = None):
        """Initialize evaluator from config.

        All settings loaded from configs/evaluation.yaml.
        Override via environment variables with EVALUATION__ prefix.

        Args:
            config: Optional Dynaconf config object (loads default if None)
        """
        logger.info("Initializing TriageEvaluator from config")

        # Load config
        self.config = config or get_evaluation_config()

        # Get API URL
        self.api_url = self.config.get(
            "evaluation.api_url", "http://localhost:8000"
        )
        logger.info(f"Using API URL: {self.api_url}")

        # Initialize LLM client for evaluation
        self.llm_client = self._create_llm_client()

        # Initialize Langfuse client
        self.langfuse_client = self._create_langfuse_client()

        # Initialize LLM Judge
        self.llm_judge = LLMJudge(
            llm_client=self.llm_client,
            langfuse_client=self.langfuse_client,
        )

        # Initialize Workflow Validator
        self.workflow_validator = WorkflowValidator(
            langfuse_client=self.langfuse_client
        )

        logger.info("TriageEvaluator ready")

    def _create_llm_client(self) -> Any:
        """Create LLM client for evaluation prompts.

        Returns:
            LLM client instance
        """
        try:
            from libs.llm.client.litellm.main import LLMClient

            llm_config = self.config.get("evaluation.llm", {})

            return LLMClient(
                proxy_url=llm_config.get("proxy_url"),
                api_key=llm_config.get("api_key"),
                completion_model=llm_config.get("model", "gpt-4"),
                temperature=llm_config.get("temperature", 0.0),
                max_tokens=llm_config.get("max_tokens", 2000),
            )

        except Exception as e:
            logger.warning(f"Failed to create LLM client: {e}")
            return None

    def _create_langfuse_client(self) -> Optional[Langfuse]:
        """Create Langfuse client for observability.

        Returns:
            Langfuse client instance or None if not configured
        """
        try:
            langfuse_config = self.config.get(
                "evaluation.observability.langfuse", {}
            )

            public_key = langfuse_config.get("public_key")
            secret_key = langfuse_config.get("secret_key")
            host = langfuse_config.get("host", "https://cloud.langfuse.com")

            if not public_key or not secret_key:
                logger.warning(
                    "Langfuse keys not configured. "
                    "Workflow validation and score logging disabled."
                )
                return None

            return Langfuse(
                public_key=public_key,
                secret_key=secret_key,
                host=host,
            )

        except Exception as e:
            logger.warning(f"Failed to create Langfuse client: {e}")
            return None

    def run_scenario(self, scenario: TriageScenario) -> Optional[Dict[str, Any]]:
        """Run a scenario through the triage API.

        Builds a ticket payload from the scenario and sends it to the
        /api/triage endpoint.

        Args:
            scenario: TriageScenario object with ticket data

        Returns:
            API response dict with triage result, or None if failed
        """
        logger.info(f"Running scenario: {scenario.name}")

        # Build unique session/ticket ID for this evaluation run
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        ticket_id = f"eval-{scenario.id}-{timestamp}"

        # Build ticket payload matching the API schema
        payload = {
            "ticket_id": ticket_id,
            "customer_id": f"eval-customer-{scenario.id}",
            "customer_info": {
                "plan": scenario.customer_profile.plan,
                "tenure_months": scenario.customer_profile.tenure_months,
                "region": scenario.customer_profile.region,
                "seats": scenario.customer_profile.seats,
                "previous_tickets": scenario.customer_profile.previous_tickets,
            },
            "messages": [
                {
                    "role": msg.role,
                    "content": msg.content,
                    "timestamp": msg.timestamp,
                }
                for msg in scenario.messages
            ],
        }

        try:
            response = requests.post(
                f"{self.api_url}/api/triage",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=120,  # Allow longer timeout for LLM processing
            )

            if response.status_code != 200:
                logger.error(
                    f"API request failed: {response.status_code} - {response.text}"
                )
                return None

            result = response.json()
            result["ticket_id"] = ticket_id
            result["session_id"] = ticket_id  # For Langfuse trace lookup
            return result

        except requests.exceptions.Timeout:
            logger.error(f"API request timed out for scenario: {scenario.name}")
            return None

        except Exception as e:
            logger.error(f"API request failed: {e}")
            return None

    def evaluate_classification_accuracy(
        self,
        scenario: TriageScenario,
        result: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Evaluate classification accuracy (deterministic).

        Compares actual vs expected for:
        - Urgency level (critical/high/medium/low)
        - Ticket type routing (billing/technical/general)
        - Recommended action (auto_respond/route_specialist/escalate_human)
        - Language detection

        Args:
            scenario: Scenario with expectations
            result: API triage result

        Returns:
            Classification accuracy scores (each 0 or 1)
        """
        expected = scenario.expected_triage

        # Extract actual values from result
        actual_urgency = result.get("urgency", "").lower()
        actual_action = result.get("recommended_action", "").lower()
        extracted_info = result.get("extracted_info", {})
        actual_type = extracted_info.get("product_area", "").lower()
        actual_language = extracted_info.get("language", "en").lower()

        # Calculate exact matches
        urgency_match = actual_urgency == expected.expected_urgency.value
        action_match = actual_action == expected.expected_action.value
        type_match = actual_type == expected.expected_ticket_type.lower()
        language_match = actual_language == expected.expected_language.lower()

        return {
            "urgency_accuracy": 1.0 if urgency_match else 0.0,
            "action_accuracy": 1.0 if action_match else 0.0,
            "routing_accuracy": 1.0 if type_match else 0.0,
            "language_accuracy": 1.0 if language_match else 0.0,
            "details": {
                "urgency": {
                    "expected": expected.expected_urgency.value,
                    "actual": actual_urgency,
                    "match": urgency_match,
                },
                "action": {
                    "expected": expected.expected_action.value,
                    "actual": actual_action,
                    "match": action_match,
                },
                "type": {
                    "expected": expected.expected_ticket_type,
                    "actual": actual_type,
                    "match": type_match,
                },
                "language": {
                    "expected": expected.expected_language,
                    "actual": actual_language,
                    "match": language_match,
                },
            },
        }

    def evaluate_triage_quality(
        self,
        scenario: TriageScenario,
        result: Dict[str, Any],
    ) -> Optional[Dict[str, Any]]:
        """Evaluate triage result quality using LLM judge.

        Args:
            scenario: Scenario with expectations
            result: API triage result

        Returns:
            Quality scores dict or None if failed
        """
        session_id = result.get("session_id")

        try:
            scores = self.llm_judge.evaluate_triage_quality(
                scenario=scenario,
                triage_result=result,
                session_id=session_id,
            )
            return scores

        except Exception as e:
            logger.error(f"Quality evaluation failed: {e}", exc_info=True)
            return None

    def run_all_scenarios(
        self,
        waiting_time: int = 30,
        categories: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """Run all evaluation scenarios.

        Executes each scenario through the API, validates workflow,
        and evaluates quality. Results are logged to Langfuse.

        Args:
            waiting_time: Seconds to wait for Langfuse trace submission
            categories: Optional list of categories to filter (e.g., ["billing", "technical"])

        Returns:
            List of evaluation results with workflow and quality scores
        """
        logger.info("Starting evaluation of all scenarios")
        results = []

        # Collect all scenarios
        all_scenarios = [
            *[(s, "billing") for s in billing.SCENARIOS],
            *[(s, "technical") for s in technical.SCENARIOS],
            *[(s, "general") for s in general.SCENARIOS],
            *[(s, "escalation") for s in escalation.SCENARIOS],
            *[(s, "multilingual") for s in multilingual.SCENARIOS],
            *[(s, "edge_cases") for s in edge_cases.SCENARIOS],
        ]

        # Filter by categories if specified
        if categories:
            all_scenarios = [
                (s, c) for s, c in all_scenarios if c in categories
            ]

        print(f"\nTotal scenarios to evaluate: {len(all_scenarios)}")
        print("-" * 60)

        for idx, (scenario, category) in enumerate(all_scenarios, 1):
            print(f"\n[{idx}/{len(all_scenarios)}] Running: {scenario.name} ({category})")
            logger.info(f"Running scenario: {scenario.name} ({category})")

            # Run scenario through API
            print("  -> Sending ticket to API...")
            result = self.run_scenario(scenario)

            if not result:
                print("  X API call failed")
                results.append({
                    "scenario": scenario.name,
                    "scenario_id": scenario.id,
                    "category": category,
                    "success": False,
                    "error": "API call failed",
                })
                continue

            session_id = result.get("session_id")
            print(f"  -> Session ID: {session_id}")

            # Wait for Langfuse trace to propagate
            print(f"  -> Waiting {waiting_time}s for trace submission...")
            time.sleep(waiting_time)

            # 1. Classification Accuracy (deterministic)
            print("  -> Evaluating classification accuracy...")
            classification = self.evaluate_classification_accuracy(scenario, result)
            urgency_ok = classification["details"]["urgency"]["match"]
            routing_ok = classification["details"]["type"]["match"]
            action_ok = classification["details"]["action"]["match"]
            print(
                f"  -> Classification: urgency={'OK' if urgency_ok else 'MISS'}, "
                f"routing={'OK' if routing_ok else 'MISS'}, "
                f"action={'OK' if action_ok else 'MISS'}"
            )

            # 2. Workflow Validation
            print("  -> Validating workflow...")
            workflow_result = self.workflow_validator.validate(scenario, session_id)
            workflow_pass = (
                workflow_result.get("pass", False) if workflow_result else False
            )
            print(f"  -> Workflow: {'PASS' if workflow_pass else 'FAIL'}")

            if not workflow_pass and workflow_result:
                agents_info = workflow_result.get("agents", {})
                tools_info = workflow_result.get("tools", {})
                if agents_info.get("missing"):
                    print(f"     Missing agents: {agents_info['missing']}")
                if tools_info.get("missing"):
                    print(f"     Missing tools: {tools_info['missing']}")

            # 3. Quality Evaluation (LLM Judge)
            print("  -> Evaluating quality with LLM judge...")
            quality_scores = self.evaluate_triage_quality(scenario, result)

            if quality_scores and "error" not in quality_scores:
                aq = quality_scores.get("answer_quality", 0)
                fc = quality_scores.get("factual_correctness", 0)
                cp = quality_scores.get("completeness", 0)
                print(f"  -> Quality: answer={aq:.2f}, factual={fc:.2f}, complete={cp:.2f}")
            else:
                print("  -> Quality evaluation failed or skipped")

            # Store results
            results.append({
                "scenario": scenario.name,
                "scenario_id": scenario.id,
                "category": category,
                "success": True,
                "session_id": session_id,
                "classification": classification,
                "workflow": workflow_result,
                "quality": quality_scores,
                "raw_result": result,
            })

        # Flush Langfuse traces
        print(f"\n{'=' * 60}")
        print("Flushing traces to Langfuse...")

        if self.langfuse_client:
            try:
                self.langfuse_client.flush()
                print("Traces flushed successfully")
            except Exception as e:
                print(f"Warning: Failed to flush traces: {e}")

        # Print summary
        self._print_summary(results)

        return results

    def _print_summary(self, results: List[Dict[str, Any]]):
        """Print evaluation summary statistics.

        Args:
            results: List of evaluation results
        """
        print("\n" + "=" * 60)
        print("EVALUATION SUMMARY")
        print("=" * 60)

        total = len(results)
        successful = sum(1 for r in results if r.get("success"))
        workflow_passed = sum(
            1 for r in results if r.get("workflow", {}).get("pass", False)
        )

        # Classification averages
        urgency_scores = [
            r["classification"]["urgency_accuracy"]
            for r in results
            if r.get("classification")
        ]
        routing_scores = [
            r["classification"]["routing_accuracy"]
            for r in results
            if r.get("classification")
        ]
        action_scores = [
            r["classification"]["action_accuracy"]
            for r in results
            if r.get("classification")
        ]

        # Quality averages
        quality_scores = [
            r["quality"].get("answer_quality", 0)
            for r in results
            if r.get("quality") and "error" not in r.get("quality", {})
        ]

        print(f"\nTotal Scenarios: {total}")
        print(f"Successful Runs: {successful}/{total}")
        print(f"Workflow Passed: {workflow_passed}/{total}")

        if urgency_scores:
            print(f"\nClassification Accuracy:")
            print(f"  Urgency:  {sum(urgency_scores)/len(urgency_scores):.1%}")
            print(f"  Routing:  {sum(routing_scores)/len(routing_scores):.1%}")
            print(f"  Action:   {sum(action_scores)/len(action_scores):.1%}")

        if quality_scores:
            print(f"\nQuality Scores (avg):")
            print(f"  Answer Quality: {sum(quality_scores)/len(quality_scores):.2f}")

        # Per-category breakdown
        print(f"\nBy Category:")
        categories = set(r["category"] for r in results)
        for cat in sorted(categories):
            cat_results = [r for r in results if r["category"] == cat]
            cat_success = sum(1 for r in cat_results if r.get("success"))
            cat_urgency = [
                r["classification"]["urgency_accuracy"]
                for r in cat_results
                if r.get("classification")
            ]
            avg_urgency = sum(cat_urgency) / len(cat_urgency) if cat_urgency else 0
            print(f"  {cat}: {cat_success}/{len(cat_results)} success, {avg_urgency:.1%} urgency accuracy")

        print("=" * 60)

"""LLM-as-a-Judge evaluation for triage quality.

Evaluates agent responses using LLM-based scoring with prompts from Langfuse.
Logs scores to Langfuse for tracking and analysis.
"""

import json
from typing import Any, Dict, List, Optional

from langfuse import Langfuse

from evaluation.scenarios.base import TriageScenario
from libs.logger.logger import get_logger

logger = get_logger(__name__)


class LLMJudge:
    """LLM-as-a-Judge evaluator for triage quality.

    Uses Langfuse-managed prompts for evaluation criteria.
    Logs scores back to Langfuse for quality monitoring.

    Evaluation metrics (all 0-1 scale):
    - answer_quality: Reasoning clarity and professionalism
    - factual_correctness: Accuracy of classifications
    - completeness: Coverage of expected criteria
    - language_detection: Correct language identified
    - translation_accuracy: Meaning preserved in translation
    - kb_relevance: Relevance of KB articles returned

    Example:
        >>> judge = LLMJudge(llm_client, langfuse_client)
        >>> scores = judge.evaluate_triage_quality(scenario, result, session_id)
        >>> print(scores['answer_quality'])  # 0.85
    """

    def __init__(
        self,
        llm_client: Any,
        langfuse_client: Optional[Langfuse] = None,
    ):
        """Initialize LLM Judge.

        Args:
            llm_client: LLM client for running evaluation prompts
            langfuse_client: Optional Langfuse client for prompts and scoring
        """
        self.llm_client = llm_client
        self.langfuse_client = langfuse_client
        logger.info("LLMJudge initialized")

    def load_evaluation_prompt(self, prompt_name: str, label: str = "production") -> str:
        """Load evaluation prompt from Langfuse.

        Fetches the prompt template from Langfuse by name and label.
        Prompts should be uploaded using the upload_evaluation_prompts.py script.

        Args:
            prompt_name: Prompt name (e.g., "evaluation_triage_quality")
            label: Prompt label/version (default: "production")

        Returns:
            Prompt template string with {{variable}} placeholders

        Raises:
            ValueError: If prompt not found in Langfuse
        """
        if not self.langfuse_client:
            raise ValueError("Langfuse client not available")

        try:
            prompt_obj = self.langfuse_client.get_prompt(
                name=prompt_name,
                label=label,
            )
            return prompt_obj.prompt

        except Exception as e:
            logger.error(f"Failed to load prompt '{prompt_name}': {e}")
            raise ValueError(
                f"Evaluation prompt '{prompt_name}' not found in Langfuse. "
                f"Upload prompts first: python scripts/upload_evaluation_prompts.py"
            )

    def fill_template(self, template: str, variables: Dict[str, Any]) -> str:
        """Fill template with variables using {{variable}} syntax.

        Args:
            template: Template string with {{variable}} placeholders
            variables: Dictionary of variable values

        Returns:
            Filled template string
        """
        result = template
        for key, value in variables.items():
            placeholder = f"{{{{{key}}}}}"
            # Convert non-string values to JSON for readability
            if isinstance(value, (dict, list)):
                value = json.dumps(value, indent=2, default=str)
            result = result.replace(placeholder, str(value))
        return result

    def evaluate_triage_quality(
        self,
        scenario: TriageScenario,
        triage_result: Dict[str, Any],
        session_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Evaluate overall triage quality.

        Uses LLM to judge the quality of triage reasoning, classification
        accuracy, and completeness against expected criteria.

        Metrics:
        - answer_quality: Reasoning clarity and professionalism
        - factual_correctness: Accuracy of extracted information
        - completeness: Coverage of expected criteria

        Args:
            scenario: Scenario with expectations
            triage_result: API triage result
            session_id: Langfuse session for score logging

        Returns:
            Quality scores dict with values 0-1 and reasoning
        """
        logger.info(f"Evaluating triage quality for: {scenario.name}")

        try:
            # Load prompt template from Langfuse
            template = self.load_evaluation_prompt("evaluation_triage_quality")
        except ValueError:
            # Fallback to local evaluation if prompt not available
            logger.warning("Using fallback evaluation (Langfuse prompt not available)")
            return self._fallback_quality_evaluation(scenario, triage_result)

        # Build context for evaluation
        prompt = self.fill_template(
            template,
            {
                "scenario_name": scenario.name,
                "scenario_description": scenario.description,
                "ticket_messages": [
                    {"role": m.role, "content": m.content} for m in scenario.messages
                ],
                "customer_profile": {
                    "plan": scenario.customer_profile.plan,
                    "tenure_months": scenario.customer_profile.tenure_months,
                    "region": scenario.customer_profile.region,
                    "seats": scenario.customer_profile.seats,
                    "previous_tickets": scenario.customer_profile.previous_tickets,
                },
                "expected_criteria": scenario.expected_answer_criteria,
                "actual_result": triage_result,
                "expected_urgency": scenario.expected_triage.expected_urgency.value,
                "expected_action": scenario.expected_triage.expected_action.value,
                "expected_type": scenario.expected_triage.expected_ticket_type,
            },
        )

        # Run evaluation
        response = self.llm_client.generate(prompt=prompt)

        # Parse JSON response
        try:
            scores = self._parse_json_response(response)
            logger.info(f"Triage quality evaluation: {scores}")

            # Log to Langfuse
            if self.langfuse_client and session_id:
                self._log_scores_to_langfuse(
                    session_id=session_id,
                    category="triage_quality",
                    scores=scores,
                )

            return scores

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse evaluation JSON: {e}")
            return {
                "answer_quality": 0.0,
                "factual_correctness": 0.0,
                "completeness": 0.0,
                "reasoning": "Failed to parse evaluation response",
                "error": str(e),
            }

    def evaluate_translation_accuracy(
        self,
        scenario: TriageScenario,
        triage_result: Dict[str, Any],
        session_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Evaluate translation accuracy for non-English tickets.

        Metrics:
        - language_detection: Correct language identified (0 or 1)
        - translation_accuracy: Meaning preserved in translation (0-1)
        - context_preservation: Important details retained (0-1)

        Args:
            scenario: Scenario with expected language
            triage_result: API triage result
            session_id: Langfuse session for score logging

        Returns:
            Translation scores dict
        """
        logger.info(f"Evaluating translation for: {scenario.name}")

        # Quick check: is this a multilingual scenario?
        expected_language = scenario.expected_triage.expected_language
        if expected_language == "en":
            return {
                "language_detection": 1.0,
                "translation_accuracy": 1.0,
                "context_preservation": 1.0,
                "reasoning": "English ticket, no translation needed",
            }

        try:
            template = self.load_evaluation_prompt("evaluation_translation")
        except ValueError:
            logger.warning("Using fallback translation evaluation")
            return self._fallback_translation_evaluation(scenario, triage_result)

        original_message = scenario.messages[0].content if scenario.messages else ""
        detected_language = (
            triage_result.get("extracted_info", {}).get("language", "unknown")
        )

        prompt = self.fill_template(
            template,
            {
                "original_message": original_message,
                "expected_language": expected_language,
                "detected_language": detected_language,
                "triage_reasoning": triage_result.get("reasoning", ""),
            },
        )

        response = self.llm_client.generate(prompt=prompt)

        try:
            scores = self._parse_json_response(response)

            if self.langfuse_client and session_id:
                self._log_scores_to_langfuse(
                    session_id=session_id,
                    category="translation",
                    scores=scores,
                )

            return scores

        except json.JSONDecodeError:
            return {
                "language_detection": 0.0,
                "translation_accuracy": 0.0,
                "context_preservation": 0.0,
                "error": "Failed to parse translation evaluation",
            }

    def evaluate_kb_relevance(
        self,
        scenario: TriageScenario,
        triage_result: Dict[str, Any],
        session_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Evaluate KB article relevance.

        Metrics:
        - articles_found: Whether relevant articles were returned
        - relevance_quality: Quality of article matches
        - coverage: Whether articles address the issue

        Args:
            scenario: Scenario with KB expectations
            triage_result: API triage result
            session_id: Langfuse session for score logging

        Returns:
            KB relevance scores dict
        """
        logger.info(f"Evaluating KB relevance for: {scenario.name}")

        relevant_articles = triage_result.get("relevant_articles", [])
        expected = scenario.expected_triage

        # Basic checks
        has_articles = len(relevant_articles) > 0
        articles_expected = expected.should_have_kb_articles

        # Case: Expected no articles and got none
        if not articles_expected and not has_articles:
            return {
                "articles_found": 1.0,
                "relevance_quality": 1.0,
                "coverage": 1.0,
                "reasoning": "No articles expected and none returned (escalation scenario)",
            }

        # Case: Expected articles but got none
        if articles_expected and not has_articles:
            return {
                "articles_found": 0.0,
                "relevance_quality": 0.0,
                "coverage": 0.0,
                "reasoning": "Expected KB articles but none returned",
            }

        # Case: Got articles when not expected (not necessarily wrong)
        if not articles_expected and has_articles:
            return {
                "articles_found": 0.5,
                "relevance_quality": 0.5,
                "coverage": 0.5,
                "reasoning": "KB articles returned but not expected for escalation",
            }

        # For cases with articles, use LLM to judge relevance
        try:
            template = self.load_evaluation_prompt("evaluation_kb_relevance")
        except ValueError:
            logger.warning("Using fallback KB evaluation")
            return self._fallback_kb_evaluation(scenario, triage_result)

        prompt = self.fill_template(
            template,
            {
                "ticket_content": (
                    scenario.messages[0].content if scenario.messages else ""
                ),
                "ticket_type": expected.expected_ticket_type,
                "articles": relevant_articles,
            },
        )

        response = self.llm_client.generate(prompt=prompt)

        try:
            scores = self._parse_json_response(response)

            if self.langfuse_client and session_id:
                self._log_scores_to_langfuse(
                    session_id=session_id,
                    category="kb_relevance",
                    scores=scores,
                )

            return scores

        except json.JSONDecodeError:
            return {"error": "Failed to parse KB relevance evaluation"}

    def _parse_json_response(self, response: str) -> Dict[str, Any]:
        """Parse JSON from LLM response.

        Handles markdown code blocks that LLMs often wrap JSON in.

        Args:
            response: Raw LLM response text

        Returns:
            Parsed JSON dict

        Raises:
            json.JSONDecodeError: If response cannot be parsed as JSON
        """
        content = response.strip()

        # Handle markdown code blocks
        if content.startswith("```json"):
            content = content.split("```json")[1].split("```")[0].strip()
        elif content.startswith("```"):
            lines = content.split("\n")
            content = "\n".join(
                [line for line in lines if not line.startswith("```")]
            )

        return json.loads(content)

    def _log_scores_to_langfuse(
        self,
        session_id: str,
        category: str,
        scores: Dict[str, Any],
    ):
        """Log evaluation scores to Langfuse.

        Creates individual score entries for each metric and an
        overall category score (average of numeric metrics).

        Args:
            session_id: Session ID for trace linking
            category: Score category prefix (e.g., "triage_quality")
            scores: Scores dictionary with metric names as keys
        """
        if not self.langfuse_client:
            return

        try:
            # Log individual metric scores
            numeric_scores = []
            for metric_name, score_value in scores.items():
                if metric_name in ("reasoning", "error"):
                    continue

                if isinstance(score_value, (int, float)):
                    numeric_scores.append(score_value)
                    self.langfuse_client.create_score(
                        name=f"{category}_{metric_name}",
                        value=score_value,
                        trace_id=session_id,
                        comment=scores.get("reasoning", ""),
                    )

            # Log overall category score (average of metrics)
            if numeric_scores:
                overall_score = sum(numeric_scores) / len(numeric_scores)
                self.langfuse_client.create_score(
                    name=f"{category}_overall",
                    value=overall_score,
                    trace_id=session_id,
                    comment=f"Average of {len(numeric_scores)} metrics. "
                    f"{scores.get('reasoning', '')}",
                )

            # Flush to ensure scores are sent
            self.langfuse_client.flush()
            logger.info(
                f"Logged {len(numeric_scores) + 1} scores to Langfuse "
                f"for session {session_id}"
            )

        except Exception as e:
            logger.warning(f"Failed to log scores to Langfuse: {e}")

    def _fallback_quality_evaluation(
        self,
        scenario: TriageScenario,
        triage_result: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Fallback quality evaluation without Langfuse prompts.

        Performs basic deterministic checks when LLM evaluation
        is not available.

        Args:
            scenario: Scenario with expectations
            triage_result: API triage result

        Returns:
            Basic quality scores
        """
        expected = scenario.expected_triage

        # Check urgency match
        actual_urgency = triage_result.get("urgency", "").lower()
        urgency_match = actual_urgency == expected.expected_urgency.value

        # Check action match
        actual_action = triage_result.get("recommended_action", "").lower()
        action_match = actual_action == expected.expected_action.value

        # Check type match
        extracted_info = triage_result.get("extracted_info", {})
        actual_type = extracted_info.get("product_area", "").lower()
        type_match = actual_type == expected.expected_ticket_type.lower()

        # Calculate scores
        matches = sum([urgency_match, action_match, type_match])
        score = matches / 3.0

        return {
            "answer_quality": score,
            "factual_correctness": score,
            "completeness": score,
            "reasoning": f"Fallback evaluation: {matches}/3 classifications correct",
        }

    def _fallback_translation_evaluation(
        self,
        scenario: TriageScenario,
        triage_result: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Fallback translation evaluation."""
        expected_lang = scenario.expected_triage.expected_language
        detected_lang = (
            triage_result.get("extracted_info", {}).get("language", "unknown")
        )
        lang_match = expected_lang.lower() == detected_lang.lower()

        return {
            "language_detection": 1.0 if lang_match else 0.0,
            "translation_accuracy": 0.5,  # Cannot evaluate without LLM
            "context_preservation": 0.5,
            "reasoning": f"Fallback: language {'matched' if lang_match else 'mismatch'}",
        }

    def _fallback_kb_evaluation(
        self,
        scenario: TriageScenario,
        triage_result: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Fallback KB relevance evaluation."""
        articles = triage_result.get("relevant_articles", [])
        has_articles = len(articles) > 0
        expected_articles = scenario.expected_triage.should_have_kb_articles

        if has_articles == expected_articles:
            return {
                "articles_found": 1.0,
                "relevance_quality": 0.5,  # Cannot evaluate quality without LLM
                "coverage": 0.5,
                "reasoning": "Fallback: article presence matches expectation",
            }
        else:
            return {
                "articles_found": 0.0,
                "relevance_quality": 0.0,
                "coverage": 0.0,
                "reasoning": "Fallback: article presence mismatch",
            }

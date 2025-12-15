#!/usr/bin/env python3
"""Run LLM-as-a-Judge evaluation on triage scenarios.

Executes test scenarios against the triage API, validates workflows,
and evaluates quality using LLM-based scoring with Langfuse integration.

Usage:
    # Run all scenarios
    python scripts/run_triage_evaluation.py

    # Run specific category
    python scripts/run_triage_evaluation.py --category billing

    # Run with custom wait time
    python scripts/run_triage_evaluation.py --wait-time 45

    # Run specific scenario
    python scripts/run_triage_evaluation.py --scenario billing-01-double-charge

Environment Variables:
    EVALUATION_API_URL: API endpoint (default: http://localhost:8000)
    LANGFUSE_PUBLIC_KEY: Required for workflow validation
    LANGFUSE_SECRET_KEY: Required for workflow validation
    LITELLM_PROXY_URL: LLM proxy for evaluation judge
    LITELLM_API_KEY: LLM API key
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from libs.logger.logger import get_logger, setup_logging

logger = get_logger(__name__)


def main() -> int:
    """Run triage evaluation scenarios.

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    parser = argparse.ArgumentParser(
        description="Run LLM-as-a-Judge evaluation on triage scenarios"
    )
    parser.add_argument(
        "--category",
        type=str,
        choices=["billing", "technical", "general", "escalation", "multilingual", "edge_cases"],
        help="Run only scenarios from a specific category",
    )
    parser.add_argument(
        "--scenario",
        type=str,
        help="Run only a specific scenario by ID (e.g., billing-01-double-charge)",
    )
    parser.add_argument(
        "--wait-time",
        type=int,
        default=30,
        help="Seconds to wait for Langfuse traces after each API call (default: 30)",
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Path to write JSON results file",
    )
    parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging level (default: INFO)",
    )
    args = parser.parse_args()

    # Setup logging
    setup_logging(level=args.log_level)

    try:
        print("\n" + "=" * 60)
        print("Support Ticket Triage - LLM Evaluation Runner")
        print("=" * 60 + "\n")

        logger.info("Starting triage evaluation")

        # Import here to avoid import errors if dependencies missing
        from evaluation.evaluator import TriageEvaluator

        # Initialize evaluator
        print("Initializing evaluator...")
        evaluator = TriageEvaluator()

        print(f"  API URL: {evaluator.api_url}")
        print(f"  LLM Client: {'Available' if evaluator.llm_client else 'Not configured'}")
        print(f"  Langfuse: {'Connected' if evaluator.langfuse_client else 'Not configured'}")
        print(f"  Wait Time: {args.wait_time}s\n")

        # Determine which categories to run
        categories = None
        if args.category:
            categories = [args.category]
            print(f"Running category: {args.category}")
        else:
            print("Running all categories")

        # Run scenarios
        print(f"\nStarting evaluation (wait time: {args.wait_time}s per scenario)...\n")
        results = evaluator.run_all_scenarios(
            waiting_time=args.wait_time,
            categories=categories,
        )

        # Filter by specific scenario if requested
        if args.scenario:
            results = [r for r in results if r.get("scenario_id") == args.scenario]
            if not results:
                print(f"\nNo results found for scenario: {args.scenario}")
                return 1

        # Output detailed results
        print("\n" + "=" * 60)
        print("DETAILED RESULTS")
        print("=" * 60)

        for result in results:
            print(f"\n{result['scenario']} ({result['category']}):")
            print(f"  Scenario ID: {result.get('scenario_id', 'N/A')}")
            print(f"  Session ID: {result.get('session_id', 'N/A')}")

            if not result.get("success"):
                print(f"  Status: FAILED - {result.get('error', 'Unknown error')}")
                continue

            # Classification results
            if "classification" in result:
                cls = result["classification"]
                print("  Classification:")
                for key in ["urgency", "action", "type", "language"]:
                    if key in cls.get("details", {}):
                        detail = cls["details"][key]
                        status = "MATCH" if detail.get("match") else "MISMATCH"
                        print(f"    {key.title()}: {detail.get('actual', 'N/A')} "
                              f"(expected: {detail.get('expected', 'N/A')}) [{status}]")

            # Workflow results
            if "workflow" in result and result["workflow"]:
                wf = result["workflow"]
                wf_status = "PASS" if wf.get("pass") else "FAIL"
                print(f"  Workflow: {wf_status}")
                if not wf.get("pass"):
                    agents = wf.get("agents", {})
                    tools = wf.get("tools", {})
                    if agents.get("missing"):
                        print(f"    Missing agents: {agents['missing']}")
                    if agents.get("unwanted"):
                        print(f"    Unwanted agents: {agents['unwanted']}")
                    if tools.get("missing"):
                        print(f"    Missing tools: {tools['missing']}")
                    if tools.get("unwanted"):
                        print(f"    Unwanted tools: {tools['unwanted']}")

            # Quality results
            if "quality" in result and result["quality"]:
                q = result["quality"]
                if "error" not in q:
                    print("  Quality Scores:")
                    for metric, value in q.items():
                        if metric != "reasoning" and isinstance(value, (int, float)):
                            print(f"    {metric}: {value:.2f}")
                    if "reasoning" in q:
                        print(f"    Reasoning: {q['reasoning'][:100]}...")

        # Write results to file if requested
        if args.output:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Prepare serializable results
            output_data = {
                "timestamp": datetime.now().isoformat(),
                "config": {
                    "api_url": evaluator.api_url,
                    "wait_time": args.wait_time,
                    "category_filter": args.category,
                    "scenario_filter": args.scenario,
                },
                "results": results,
            }

            with open(output_path, "w") as f:
                json.dump(output_data, f, indent=2, default=str)

            print(f"\nResults written to: {output_path}")

        print("\n" + "=" * 60)
        print("View detailed traces at your Langfuse dashboard")
        print("=" * 60 + "\n")

        # Return success if all scenarios passed
        failed_count = sum(1 for r in results if not r.get("success"))
        return 0 if failed_count == 0 else 1

    except ImportError as e:
        logger.error(f"Import error - check dependencies: {e}")
        print(f"\nError: Missing dependencies. Run: pip install -r requirements.txt")
        return 1

    except Exception as e:
        logger.error(f"Evaluation failed: {e}", exc_info=True)
        print(f"\nError: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

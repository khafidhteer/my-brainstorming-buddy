"""Fault Tree Analysis (FTA) Framework.

A deductive, top-down approach to analyze system failures using
AND/OR logic gates. Steps:
1. Define the top undesired event
2. Identify intermediate events (OR/AND logic)
3. Trace to basic events (root causes)
4. Recommend preventive measures
"""

from typing import List
from src.frameworks.base import BaseFramework, StepDefinition


class FaultTreeFramework(BaseFramework):
    """Fault Tree Analysis framework for failure analysis."""

    @property
    def name(self) -> str:
        return "Fault Tree Analysis"

    @property
    def description(self) -> str:
        return (
            "Best for analyzing system failures and safety incidents "
            "using deductive logic. Traces a top-level failure event "
            "down through intermediate events to basic root causes "
            "using AND/OR gate logic. Ideal for engineering reliability, "
            "safety analysis, and complex system failures."
        )

    @property
    def steps(self) -> List[StepDefinition]:
        return [
            StepDefinition(
                index=0,
                name="Define Top Event",
                description="Define the top undesired event or failure to analyze",
                system_prompt=(
                    "You are an expert in Fault Tree Analysis. "
                    "Your task is to define the top-level failure event "
                    "precisely and unambiguously."
                ),
                temperature=0.5,
                max_tokens=1024,
            ),
            StepDefinition(
                index=1,
                name="Identify Intermediate Events",
                description="Break down the top event into intermediate events using AND/OR logic gates",
                system_prompt=(
                    "You are an expert in Fault Tree Analysis. "
                    "Continue the fault tree analysis. "
                    "For the top event, identify the immediate causes "
                    "and use AND gates (all conditions must be true) "
                    "or OR gates (any condition being true is sufficient) "
                    "to show how they combine. Be systematic."
                ),
                temperature=0.7,
                max_tokens=2048,
            ),
            StepDefinition(
                index=2,
                name="Trace to Basic Events",
                description="Continue decomposing until reaching basic (root cause) events",
                system_prompt=(
                    "You are an expert in Fault Tree Analysis. "
                    "Continue decomposing the intermediate events "
                    "until you reach basic events that cannot be "
                    "further decomposed. These are the root causes. "
                    "Show the logical gate relationships clearly."
                ),
                temperature=0.7,
                max_tokens=2048,
            ),
            StepDefinition(
                index=3,
                name="Recommend Preventive Measures",
                description="Based on the fault tree, recommend measures to prevent the top event",
                system_prompt=(
                    "You are an expert in Fault Tree Analysis. "
                    "Based on the complete fault tree, recommend "
                    "preventive and protective measures. "
                    "Identify critical paths and single points of failure. "
                    "Prioritize measures that address root causes "
                    "rather than symptoms."
                ),
                temperature=0.5,
                max_tokens=2048,
            ),
        ]

    def generate_prompt(
        self,
        step_index: int,
        question: str,
        previous_outputs: List[str],
    ) -> tuple[str, str]:
        step = self.get_step(step_index)
        if not step:
            raise ValueError(f"Invalid step index: {step_index}")

        if step_index == 0:
            user_prompt = (
                f"Failure/incident to analyze: {question}\n\n"
                "Define the top undesired event precisely. "
                "What is the specific failure or accident we're analyzing?"
            )
        elif step_index == 1:
            user_prompt = (
                f"Original question: {question}\n\n"
                f"Top event (from Step 1):\n{previous_outputs[0]}\n\n"
                "Break this top event into intermediate events. "
                "For each branch, specify if it's an AND or OR gate. "
                "AND = all sub-events must occur. "
                "OR = any sub-event triggers the parent."
            )
        elif step_index == 2:
            context = "\n\n".join([
                f"Step {i+1}: {out}"
                for i, out in enumerate(previous_outputs)
            ])
            user_prompt = (
                f"Original question: {question}\n\n"
                f"Fault tree so far:\n{context}\n\n"
                "Continue decomposing each intermediate event down to "
                "basic events (root causes). Show the full fault tree "
                "hierarchy with gate types."
            )
        elif step_index == 3:
            context = "\n\n".join([
                f"Step {i+1}: {out}"
                for i, out in enumerate(previous_outputs)
            ])
            user_prompt = (
                f"Original question: {question}\n\n"
                f"Complete fault tree:\n{context}\n\n"
                "Based on this fault tree, what are the most critical "
                "preventive measures? Identify minimal cut sets "
                "(smallest combination of failures that cause the top event). "
                "Recommend specific actions."
            )
        else:
            raise ValueError(f"Invalid step index: {step_index}")

        return step.system_prompt, user_prompt
"""Iceberg Model Framework.

A systems thinking approach that looks beyond surface events
to understand patterns, structures, and mental models.
Steps:
1. Identify the visible event
2. Uncover patterns of behavior
3. Identify systemic structures
4. Reveal mental models
"""

from typing import List
from src.frameworks.base import BaseFramework, StepDefinition


class IcebergFramework(BaseFramework):
    """Iceberg Model framework for systemic analysis."""

    @property
    def name(self) -> str:
        return "The Iceberg Model"

    @property
    def description(self) -> str:
        return (
            "Best for understanding deep systemic issues beyond surface events. "
            "Uses a four-level model: Events (what happened), Patterns (trends), "
            "Structures (systems that create patterns), and Mental Models "
            "(beliefs that create structures). Ideal for complex social, "
            "organizational, and systemic challenges."
        )

    @property
    def steps(self) -> List[StepDefinition]:
        return [
            StepDefinition(
                index=0,
                name="Identify the Event",
                description="Describe the visible event or symptom at the surface level",
                system_prompt=(
                    "You are an expert in systems thinking using the Iceberg Model. "
                    "Start by identifying the visible event or symptom. "
                    "This is the 'tip of the iceberg' - what is happening "
                    "that caught our attention?"
                ),
                temperature=0.5,
                max_tokens=1024,
            ),
            StepDefinition(
                index=1,
                name="Uncover Patterns",
                description="Look for patterns and trends over time beneath the event",
                system_prompt=(
                    "You are an expert in systems thinking using the Iceberg Model. "
                    "Go one level deeper. What patterns or trends are visible "
                    "over time? Look for recurring events, cycles, or trends "
                    "that the surface event is part of. Ask: What has been "
                    "happening over time?"
                ),
                temperature=0.7,
                max_tokens=1536,
            ),
            StepDefinition(
                index=2,
                name="Identify Systemic Structures",
                description="Uncover the structures that drive the patterns",
                system_prompt=(
                    "You are an expert in systems thinking using the Iceberg Model. "
                    "Go deeper to identify the systemic structures. "
                    "These include: organizational structures, policies, "
                    "processes, resource flows, information flows, "
                    "power dynamics, and feedback loops. "
                    "Ask: What structures are creating these patterns?"
                ),
                temperature=0.7,
                max_tokens=2048,
            ),
            StepDefinition(
                index=3,
                name="Reveal Mental Models",
                description="Identify the beliefs, values, and assumptions that sustain the structures",
                system_prompt=(
                    "You are an expert in systems thinking using the Iceberg Model. "
                    "Go to the deepest level. What mental models, beliefs, "
                    "values, or assumptions are holding the current structures "
                    "in place? These are often unconscious and taken for granted. "
                    "Ask: What beliefs and values create these structures? "
                    "Then propose leverage points for transformative change."
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
                f"Situation to analyze: {question}\n\n"
                "What is the visible event or symptom? "
                "Describe what is happening at the surface level."
            )
        elif step_index == 1:
            user_prompt = (
                f"Original question: {question}\n\n"
                f"Surface event (from Step 1):\n{previous_outputs[0]}\n\n"
                "What patterns or trends are visible over time? "
                "Look for recurring events, cycles, or trends. "
                "How does this event fit into larger patterns?"
            )
        elif step_index == 2:
            context = "\n\n".join([
                f"Step {i+1}: {out}"
                for i, out in enumerate(previous_outputs)
            ])
            user_prompt = (
                f"Original question: {question}\n\n"
                f"Analysis so far:\n{context}\n\n"
                "What systemic structures are creating these patterns? "
                "Consider: policies, processes, resource flows, "
                "information flows, power dynamics, feedback loops, "
                "and organizational structures."
            )
        elif step_index == 3:
            context = "\n\n".join([
                f"Step {i+1}: {out}"
                for i, out in enumerate(previous_outputs)
            ])
            user_prompt = (
                f"Original question: {question}\n\n"
                f"Full analysis:\n{context}\n\n"
                "What mental models, beliefs, and assumptions "
                "are holding the current structures in place? "
                "What would need to shift at the belief level "
                "to create lasting change? Propose leverage points."
            )
        else:
            raise ValueError(f"Invalid step index: {step_index}")

        return step.system_prompt, user_prompt
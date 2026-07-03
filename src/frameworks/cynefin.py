"""The Cynefin Framework.

A sense-making framework for classifying problems into domains
to determine the appropriate decision-making approach. Steps:
1. Classify the problem context
2. Sense/Analyze the situation
3. Respond with suitable action
4. Validate outcome & adapt
"""

from typing import List
from src.frameworks.base import BaseFramework, StepDefinition


class CynefinFramework(BaseFramework):
    """Cynefin Framework for problem classification and decision-making."""

    @property
    def name(self) -> str:
        return "The Cynefin Framework"

    @property
    def description(self) -> str:
        return (
            "Best for classifying the nature of a problem to determine "
            "the appropriate decision-making approach. Five domains: "
            "Clear (cause-effect obvious), Complicated (requires expert analysis), "
            "Complex (emergent patterns, probe-sense-respond), "
            "Chaotic (act-sense-respond to stabilize), and Disorder "
            "(unknown domain). Ideal for strategy, policy, "
            "and complex decision-making contexts."
        )

    @property
    def steps(self) -> List[StepDefinition]:
        return [
            StepDefinition(
                index=0,
                name="Classify the Context",
                description="Determine which Cynefin domain the problem belongs to",
                system_prompt=(
                    "You are an expert in the Cynefin Framework for sense-making "
                    "and decision-making. "
                    "Your task is to classify the problem into one of five domains: "
                    "1) Clear - Cause and effect is obvious to all; best practice applies "
                    "2) Complicated - Cause and effect requires expert diagnosis; "
                    "good practice applies "
                    "3) Complex - Cause and effect only clear in retrospect; "
                    "emergent patterns; probe-sense-respond "
                    "4) Chaotic - Cause and effect unclear at system level; "
                    "act-sense-respond to stabilize "
                    "5) Disorder - Unknown which domain applies; first step is to gather info "
                    "Explain your reasoning for the classification."
                ),
                temperature=0.5,
                max_tokens=1536,
            ),
            StepDefinition(
                index=1,
                name="Sense and Analyze",
                description="Apply the appropriate sense-making approach based on the domain",
                system_prompt=(
                    "You are an expert in the Cynefin Framework. "
                    "Based on the domain classification, apply the appropriate approach: "
                    "- Clear: Sense -> Categorize -> Respond (apply best practice) "
                    "- Complicated: Sense -> Analyze -> Respond (apply good practice, "
                    "consult experts) "
                    "- Complex: Probe -> Sense -> Respond (run experiments, "
                    "let patterns emerge) "
                    "- Chaotic: Act -> Sense -> Respond (act quickly to stabilize, "
                    "then move to complex) "
                    "Describe how this approach would be applied to the specific situation."
                ),
                temperature=0.7,
                max_tokens=2048,
            ),
            StepDefinition(
                index=2,
                name="Respond with Action",
                description="Define the specific response and actions appropriate for this domain",
                system_prompt=(
                    "You are an expert in the Cynefin Framework. "
                    "Define specific actions appropriate for the domain: "
                    "- Clear: Standard operating procedures, checklists, best practices "
                    "- Complicated: Expert analysis, scenario planning, "
                    "multiple good practices evaluated "
                    "- Complex: Safe-to-fail experiments, probes, "
                    "feedback loops, emergent strategy "
                    "- Chaotic: Immediate action to stabilize, crisis management, "
                    "command and control "
                    "Be specific about what actions to take and why."
                ),
                temperature=0.7,
                max_tokens=2048,
            ),
            StepDefinition(
                index=3,
                name="Validate & Adapt",
                description="Validate the response and prepare to adapt as the situation evolves",
                system_prompt=(
                    "You are an expert in the Cynefin Framework. "
                    "Validate the proposed response and plan for adaptation. "
                    "Consider: "
                    "1) How will you know if the response is working? "
                    "2) What feedback loops should be monitored? "
                    "3) When might the situation shift to a different domain? "
                    "4) What are the exit criteria and escalation triggers? "
                    "5) How to prepare for domain shifts "
                    "Be practical about monitoring and adaptation."
                ),
                temperature=0.5,
                max_tokens=1536,
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
                "Which Cynefin domain does this situation belong to? "
                "Analyze: Clear, Complicated, Complex, Chaotic, or Disorder? "
                "Explain your reasoning."
            )
        elif step_index == 1:
            user_prompt = (
                f"Original question: {question}\n\n"
                f"Domain classification (from Step 1):\n{previous_outputs[0]}\n\n"
                f"Given this classification, what sense-making approach "
                f"should be applied? Describe the specific methodology."
            )
        elif step_index == 2:
            context = "\n\n".join([
                f"Step {i+1}: {out}"
                for i, out in enumerate(previous_outputs)
            ])
            user_prompt = (
                f"Original question: {question}\n\n"
                f"Analysis so far:\n{context}\n\n"
                "What specific actions should be taken given the domain? "
                "Be practical and actionable."
            )
        elif step_index == 3:
            context = "\n\n".join([
                f"Step {i+1}: {out}"
                for i, out in enumerate(previous_outputs)
            ])
            user_prompt = (
                f"Original question: {question}\n\n"
                f"Full analysis:\n{context}\n\n"
                "How should we validate that the response is working? "
                "What feedback loops should be monitored? "
                "When might the situation shift domains, and how to adapt?"
            )
        else:
            raise ValueError(f"Invalid step index: {step_index}")

        return step.system_prompt, user_prompt
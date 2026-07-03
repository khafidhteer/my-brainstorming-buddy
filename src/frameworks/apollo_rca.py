"""Apollo Root Cause Analysis Framework.

A thorough incident investigation methodology focused on
causal relationships and solution development. Steps:
1. Define the event/problem
2. Identify causal factors chain
3. Determine root causes
4. Develop solutions
5. Plan implementation
"""

from typing import List, Optional
from src.frameworks.base import BaseFramework, StepDefinition


class ApolloRCAFramework(BaseFramework):
    """Apollo Root Cause Analysis framework."""

    @property
    def name(self) -> str:
        return "Apollo Root Cause Analysis"

    @property
    def description(self) -> str:
        return (
            "Best for thorough investigation of incidents with a focus "
            "on causal relationships. Uses a structured approach to "
            "trace the chain of causality from the problem through "
            "causal factors to root causes, then develops and implements "
            "solutions. Ideal for serious incident investigations."
        )

    @property
    def steps(self) -> List[StepDefinition]:
        return [
            StepDefinition(
                index=0,
                name="Define the Event",
                description="Clearly define the problem or incident being investigated",
                system_prompt=(
                    "You are an expert in Apollo Root Cause Analysis. "
                    "Start by defining the problem or incident precisely. "
                    "Include: what happened, when it happened, where it happened, "
                    "the severity/impact, and what is known so far."
                ),
                temperature=0.5,
                max_tokens=1024,
            ),
            StepDefinition(
                index=1,
                name="Identify Causal Factors",
                description="Identify all causal factors that contributed to the event",
                system_prompt=(
                    "You are an expert in Apollo Root Cause Analysis. "
                    "Identify all causal factors that contributed to the event. "
                    "A causal factor is any condition or action that, if eliminated, "
                    "would have prevented the event or reduced its severity. "
                    "Be thorough - consider human factors, equipment, procedures, "
                    "environment, management systems, and culture."
                ),
                temperature=0.7,
                max_tokens=2048,
            ),
            StepDefinition(
                index=2,
                name="Determine Root Causes",
                description="Trace back from causal factors to identify root causes",
                system_prompt=(
                    "You are an expert in Apollo Root Cause Analysis. "
                    "For each causal factor, trace back using the '5 Whys' "
                    "technique to identify the root causes. "
                    "Root causes are the fundamental reasons why the "
                    "causal factors existed. Distinguish between: "
                    "1) Physical causes (material/equipment failures) "
                    "2) Human causes (errors, omissions) "
                    "3) Latent causes (management systems, culture, processes)"
                ),
                temperature=0.7,
                max_tokens=2048,
            ),
            StepDefinition(
                index=3,
                name="Develop Solutions",
                description="Develop specific, actionable solutions for each root cause",
                system_prompt=(
                    "You are an expert in Apollo Root Cause Analysis. "
                    "For each root cause, develop specific solutions. "
                    "Solutions should be: S.M.A.R.T. (Specific, Measurable, "
                    "Achievable, Relevant, Time-bound). "
                    "Consider both corrective actions (fix the immediate issue) "
                    "and preventive actions (prevent recurrence). "
                    "Prioritize solutions by impact and feasibility."
                ),
                temperature=0.5,
                max_tokens=2048,
            ),
            StepDefinition(
                index=4,
                name="Plan Implementation",
                description="Create an implementation plan with timelines, owners, and verification",
                system_prompt=(
                    "You are an expert in Apollo Root Cause Analysis. "
                    "Create an implementation plan for the proposed solutions. "
                    "Include: specific actions, assigned responsibilities, "
                    "timeline for completion, success criteria, "
                    "verification methods, and monitoring plan. "
                    "Also consider potential barriers to implementation "
                    "and how to overcome them."
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
                f"Incident/problem to investigate: {question}\n\n"
                "Define this incident clearly. Include: what happened, "
                "when, where, severity/impact, and what is currently known."
            )
        elif step_index == 1:
            user_prompt = (
                f"Original question: {question}\n\n"
                f"Event definition (from Step 1):\n{previous_outputs[0]}\n\n"
                "What are all the causal factors that contributed to this event? "
                "For each factor, explain how it contributed."
            )
        elif step_index == 2:
            context = "\n\n".join([
                f"Step {i+1}: {out}"
                for i, out in enumerate(previous_outputs)
            ])
            user_prompt = (
                f"Original question: {question}\n\n"
                f"Analysis so far:\n{context}\n\n"
                "For each causal factor, trace to its root cause(s). "
                "Use the 5 Whys technique. Categorize as physical, "
                "human, or latent causes."
            )
        elif step_index == 3:
            context = "\n\n".join([
                f"Step {i+1}: {out}"
                for i, out in enumerate(previous_outputs)
            ])
            user_prompt = (
                f"Original question: {question}\n\n"
                f"Analysis so far:\n{context}\n\n"
                "For each root cause, propose specific SMART solutions. "
                "Include both corrective and preventive actions."
            )
        elif step_index == 4:
            context = "\n\n".join([
                f"Step {i+1}: {out}"
                for i, out in enumerate(previous_outputs)
            ])
            user_prompt = (
                f"Original question: {question}\n\n"
                f"Full analysis:\n{context}\n\n"
                "Create an implementation plan: specific actions, "
                "who is responsible, timeline, success criteria, "
                "verification methods, and potential barriers."
            )
        else:
            raise ValueError(f"Invalid step index: {step_index}")

        return step.system_prompt, user_prompt
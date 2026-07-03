"""Fishbone Diagram (Ishikawa) Framework.

A structured approach to identify multiple root causes of a problem
by categorizing potential causes. Steps:
1. Define the problem (the "fish head")
2. Identify cause categories
3. Brainstorm sub-causes for each category
4. Identify root causes and solutions
"""

from typing import List
from src.frameworks.base import BaseFramework, StepDefinition


class FishboneFramework(BaseFramework):
    """Fishbone Diagram framework for root cause analysis."""

    @property
    def name(self) -> str:
        return "Fishbone Diagram (Ishikawa)"

    @property
    def description(self) -> str:
        return (
            "Best for identifying multiple root causes of a problem "
            "by categorizing potential causes into groups like People, "
            "Process, Equipment, Environment, Materials, and Measurement. "
            "Ideal for manufacturing, engineering, and business processes."
        )

    @property
    def steps(self) -> List[StepDefinition]:
        return [
            StepDefinition(
                index=0,
                name="Define the Problem",
                description="Clearly articulate the problem statement (the 'fish head')",
                system_prompt=(
                    "You are an expert in Fishbone (Ishikawa) root cause analysis. "
                    "Your task is to help define the problem clearly. "
                    "The problem should be specific, measurable, and actionable."
                ),
                temperature=0.5,
                max_tokens=1024,
            ),
            StepDefinition(
                index=1,
                name="Identify Cause Categories",
                description="Identify the major categories of potential causes relevant to this problem",
                system_prompt=(
                    "You are an expert in Fishbone (Ishikawa) root cause analysis. "
                    "You are continuing a root cause analysis. "
                    "Identify the major cause categories relevant to the problem. "
                    "Common categories include: People, Process, Equipment, "
                    "Environment, Materials, Measurement, Management, Policies. "
                    "Select the 4-6 most relevant categories for this specific problem."
                ),
                temperature=0.7,
                max_tokens=1536,
            ),
            StepDefinition(
                index=2,
                name="Brainstorm Sub-Causes",
                description="For each category, brainstorm specific sub-causes that could contribute to the problem",
                system_prompt=(
                    "You are an expert in Fishbone (Ishikawa) root cause analysis. "
                    "You are continuing a root cause analysis. "
                    "For each cause category identified, brainstorm specific, detailed "
                    "sub-causes. Ask 'why' repeatedly to drill down. "
                    "Be thorough and consider multiple perspectives."
                ),
                temperature=0.7,
                max_tokens=2048,
            ),
            StepDefinition(
                index=3,
                name="Identify Root Causes & Solutions",
                description="Synthesize findings to identify the most likely root causes and propose actionable solutions",
                system_prompt=(
                    "You are an expert in Fishbone (Ishikawa) root cause analysis. "
                    "You are completing a root cause analysis. "
                    "Synthesize all the findings from previous steps to: "
                    "1) Identify the 2-3 most likely root causes "
                    "2) For each root cause, propose actionable solutions "
                    "3) Suggest how to validate these root causes "
                    "Be specific and practical in your recommendations."
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
                f"Problem to analyze: {question}\n\n"
                "Please define this problem clearly. What exactly are we "
                "investigating? What is the specific symptom or defect? "
                "Include scope and impact."
            )
        elif step_index == 1:
            user_prompt = (
                f"Original problem: {question}\n\n"
                f"Problem statement (from Step 1):\n{previous_outputs[0]}\n\n"
                "What are the major cause categories for this problem? "
                "List 4-6 categories most relevant to this context."
            )
        elif step_index == 2:
            context = "\n\n".join([
                f"Step {i+1}: {out}"
                for i, out in enumerate(previous_outputs)
            ])
            user_prompt = (
                f"Original problem: {question}\n\n"
                f"Previous analysis:\n{context}\n\n"
                "For each cause category, brainstorm specific sub-causes. "
                "Use the '5 Whys' technique to drill deep."
            )
        elif step_index == 3:
            context = "\n\n".join([
                f"Step {i+1}: {out}"
                for i, out in enumerate(previous_outputs)
            ])
            user_prompt = (
                f"Original problem: {question}\n\n"
                f"Full analysis so far:\n{context}\n\n"
                "Based on all the above, what are the 2-3 most likely root causes? "
                "Propose specific solutions for each, and explain how to validate them."
            )
        else:
            raise ValueError(f"Invalid step index: {step_index}")

        return step.system_prompt, user_prompt
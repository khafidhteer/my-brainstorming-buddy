"""Ideal Customer Profile (ICP) Framework.

A framework for identifying and defining the perfect customer to target,
based on firmographic, demographic, behavioral, and needs-based criteria.
Steps:
1. Define firmographic/demographic criteria
2. Identify behavioral and engagement indicators
3. Map needs and pain points
4. Synthesize the ideal customer profile
"""

from typing import List
from src.frameworks.base import BaseFramework, StepDefinition


class IdealCustomerProfileFramework(BaseFramework):
    """Ideal Customer Profile framework by Aaron Ross."""

    @property
    def name(self) -> str:
        return "Ideal Customer Profile"

    @property
    def description(self) -> str:
        return (
            "Best for identifying and defining the perfect customer to target "
            "based on firmographic, demographic, behavioral, and needs-based criteria. "
            "Helps focus sales and marketing efforts on high-value, high-fit prospects. "
            "Ideal for B2B and B2C sales targeting, lead scoring, and marketing strategy. "
            "Introduced by Aaron Ross (Predictable Revenue)."
        )

    @property
    def steps(self) -> List[StepDefinition]:
        return [
            StepDefinition(
                index=0,
                name="Define Firmographic and Demographic Criteria",
                description="Identify the objective characteristics of your ideal customer (industry, size, location, role, etc.)",
                system_prompt=(
                    "You are an expert in Ideal Customer Profile (ICP) development "
                    "as taught by Aaron Ross in Predictable Revenue. "
                    "Your task is to define the objective criteria for your ideal customer. "
                    "For B2B: industry, company size, revenue, location, decision-maker role, budget. "
                    "For B2C: age, income, location, education, family status. "
                    "Be specific about ranges and thresholds that define 'ideal.'"
                ),
                temperature=0.5,
                max_tokens=1536,
            ),
            StepDefinition(
                index=1,
                name="Identify Behavioral and Engagement Indicators",
                description="Define the behaviors, actions, and engagement patterns of ideal customers",
                system_prompt=(
                    "You are an expert in Ideal Customer Profile (ICP) development "
                    "as taught by Aaron Ross in Predictable Revenue. "
                    "You are continuing an ICP analysis. "
                    "Identify behavioral indicators of an ideal customer: "
                    "1) Buying behaviors — purchase frequency, decision process, willingness to pay "
                    "2) Engagement patterns — how they research, what content they consume "
                    "3) Usage behaviors — how they use products like yours "
                    "4) Retention signals — what correlates with long-term loyalty "
                    "5) Referral propensity — do they refer others? "
                    "Focus on observable, measurable behaviors."
                ),
                temperature=0.7,
                max_tokens=1536,
            ),
            StepDefinition(
                index=2,
                name="Map Needs and Pain Points",
                description="Identify the specific needs, challenges, and pain points that your ideal customer experiences",
                system_prompt=(
                    "You are an expert in Ideal Customer Profile (ICP) development "
                    "as taught by Aaron Ross in Predictable Revenue. "
                    "You are continuing an ICP analysis. "
                    "Map the needs and pain points of your ideal customer: "
                    "1) What are their top 3-5 business or personal challenges? "
                    "2) What keeps them up at night? "
                    "3) What goals are they trying to achieve? "
                    "4) What solutions have they tried that failed? "
                    "5) What is the cost of not solving this problem? "
                    "6) Why would they be motivated to change? "
                    "Prioritize by urgency and willingness to pay."
                ),
                temperature=0.7,
                max_tokens=2048,
            ),
            StepDefinition(
                index=3,
                name="Synthesize the Ideal Customer Profile",
                description="Combine all criteria into a single, actionable ideal customer profile document",
                system_prompt=(
                    "You are an expert in Ideal Customer Profile (ICP) development "
                    "as taught by Aaron Ross in Predictable Revenue. "
                    "You are completing an ICP analysis. "
                    "Synthesize all findings into a single, actionable Ideal Customer Profile. "
                    "Include: 1) A one-paragraph description of the ideal customer "
                    "2) Tiered criteria (must-have, nice-to-have, disqualifiers) "
                    "3) Fit score criteria for lead scoring "
                    "4) Where to find these customers "
                    "5) How to reach them effectively "
                    "6) Common objections and how to overcome them "
                    "7) Look-alike characteristics for prospecting "
                    "Make it concrete and usable for sales and marketing teams."
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
                f"Context to analyze: {question}\n\n"
                "Define the objective characteristics of an ideal customer. "
                "Be specific: what industries, company sizes, locations, roles, "
                "or demographics are the best fit? Define ranges and thresholds."
            )
        elif step_index == 1:
            user_prompt = (
                f"Original context: {question}\n\n"
                f"Demographic/firmographic criteria (from Step 1):\n{previous_outputs[0]}\n\n"
                "Identify the behavioral indicators of an ideal customer. "
                "What patterns of buying, engagement, usage, and retention "
                "characterize your best customers? Focus on observable behaviors."
            )
        elif step_index == 2:
            context = "\n\n".join([
                f"Step {i+1}: {out}"
                for i, out in enumerate(previous_outputs)
            ])
            user_prompt = (
                f"Original context: {question}\n\n"
                f"Previous analysis:\n{context}\n\n"
                "Map the needs and pain points of the ideal customer. "
                "What are their top challenges? What motivates them to buy? "
                "What is the cost of inaction? Prioritize by urgency."
            )
        elif step_index == 3:
            context = "\n\n".join([
                f"Step {i+1}: {out}"
                for i, out in enumerate(previous_outputs)
            ])
            user_prompt = (
                f"Original context: {question}\n\n"
                f"Full analysis:\n{context}\n\n"
                "Synthesize everything into a single, actionable Ideal Customer Profile. "
                "Include tiered criteria, fit score factors, where to find them, "
                "how to reach them, common objections, and look-alike characteristics."
            )
        else:
            raise ValueError(f"Invalid step index: {step_index}")

        return step.system_prompt, user_prompt
"""Beachhead Market Strategy Framework.

A framework for identifying and capturing a single, focused market
to establish a foothold before expanding to adjacent markets.
Steps:
1. Identify potential beachhead markets
2. Evaluate and select the best beachhead
3. Develop market entry strategy
4. Plan for expansion to adjacent markets
"""

from typing import List
from src.frameworks.base import BaseFramework, StepDefinition


class BeachheadMarketFramework(BaseFramework):
    """Beachhead Market Strategy framework for market entry planning."""

    @property
    def name(self) -> str:
        return "Beachhead Market Strategy"

    @property
    def description(self) -> str:
        return (
            "Best for identifying and capturing a single, focused market "
            "to establish a foothold before expanding to adjacent markets. "
            "Focuses on selecting a market where you can dominate before scaling. "
            "Ideal for startups, new product launches, and market expansion strategy. "
            "Introduced by Bill Aulet (MIT)."
        )

    @property
    def steps(self) -> List[StepDefinition]:
        return [
            StepDefinition(
                index=0,
                name="Identify Potential Beachhead Markets",
                description="Brainstorm and list potential market segments that could serve as a beachhead",
                system_prompt=(
                    "You are an expert in Beachhead Market Strategy as taught by Bill Aulet at MIT. "
                    "Your task is to help identify potential beachhead markets. "
                    "A beachhead market is a small, specific market segment where you can "
                    "establish a dominant position before expanding. "
                    "Consider markets where: the need is urgent, customers are reachable, "
                    "and competition is weak or absent."
                ),
                temperature=0.7,
                max_tokens=1536,
            ),
            StepDefinition(
                index=1,
                name="Evaluate and Select the Best Beachhead",
                description="Evaluate each potential market against key criteria and select the best one",
                system_prompt=(
                    "You are an expert in Beachhead Market Strategy as taught by Bill Aulet at MIT. "
                    "You are continuing a market strategy analysis. "
                    "Evaluate each potential beachhead market against these criteria: "
                    "1) Size and growth potential "
                    "2) Customer urgency and willingness to pay "
                    "3) Accessibility and reachability of customers "
                    "4) Competitive landscape "
                    "5) Alignment with your capabilities "
                    "6) Potential as a platform for expansion "
                    "Score each market and recommend the best beachhead."
                ),
                temperature=0.5,
                max_tokens=2048,
            ),
            StepDefinition(
                index=2,
                name="Develop Market Entry Strategy",
                description="Create a detailed plan for entering and dominating the selected beachhead market",
                system_prompt=(
                    "You are an expert in Beachhead Market Strategy as taught by Bill Aulet at MIT. "
                    "You are continuing a market strategy analysis. "
                    "Develop a detailed entry strategy for the selected beachhead market. "
                    "Include: 1) Target customer persona within the beachhead "
                    "2) Value proposition tailored to this segment "
                    "3) Go-to-market channels and tactics "
                    "4) Pricing strategy "
                    "5) Key partnerships needed "
                    "6) Success metrics and milestones "
                    "7) Resource requirements and timeline"
                ),
                temperature=0.7,
                max_tokens=2048,
            ),
            StepDefinition(
                index=3,
                name="Plan Adjacent Market Expansion",
                description="Map out the sequence of adjacent markets to expand into after establishing the beachhead",
                system_prompt=(
                    "You are an expert in Beachhead Market Strategy as taught by Bill Aulet at MIT. "
                    "You are completing a market strategy analysis. "
                    "Plan the expansion from your beachhead to adjacent markets. "
                    "Consider: 1) Which adjacent markets are most natural to enter next? "
                    "2) What capabilities and resources from the beachhead transfer to adjacent markets? "
                    "3) What is the logical sequence of expansion? "
                    "4) How will you defend your beachhead while expanding? "
                    "5) What new capabilities will you need for each adjacent market? "
                    "Create a phased expansion roadmap."
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
                "Identify potential beachhead markets. List 3-5 specific market segments "
                "that could serve as an initial beachhead. For each, explain why it might "
                "be a good candidate — consider urgency, reachability, and competitive position."
            )
        elif step_index == 1:
            user_prompt = (
                f"Original context: {question}\n\n"
                f"Potential beachhead markets (from Step 1):\n{previous_outputs[0]}\n\n"
                "Evaluate each market against the key criteria: size, urgency, accessibility, "
                "competition, capability alignment, and expansion potential. "
                "Score each and recommend the single best beachhead market with justification."
            )
        elif step_index == 2:
            context = "\n\n".join([
                f"Step {i+1}: {out}"
                for i, out in enumerate(previous_outputs)
            ])
            user_prompt = (
                f"Original context: {question}\n\n"
                f"Previous analysis:\n{context}\n\n"
                "Develop a detailed entry strategy for the selected beachhead market. "
                "Include target persona, value proposition, go-to-market channels, "
                "pricing, partnerships, success metrics, and timeline."
            )
        elif step_index == 3:
            context = "\n\n".join([
                f"Step {i+1}: {out}"
                for i, out in enumerate(previous_outputs)
            ])
            user_prompt = (
                f"Original context: {question}\n\n"
                f"Full analysis:\n{context}\n\n"
                "Plan the expansion from your beachhead to adjacent markets. "
                "What is the logical sequence? What transfers? What new capabilities are needed? "
                "Create a phased expansion roadmap with timelines."
            )
        else:
            raise ValueError(f"Invalid step index: {step_index}")

        return step.system_prompt, user_prompt
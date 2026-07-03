"""Three Horizons of Growth Framework.

A framework for managing innovation and growth across three time horizons:
Horizon 1 (core business), Horizon 2 (emerging opportunities),
and Horizon 3 (future possibilities). Steps:
1. Analyze Horizon 1 — core business
2. Identify Horizon 2 — emerging opportunities
3. Explore Horizon 3 — future possibilities
4. Balance the portfolio across horizons
5. Create an innovation roadmap
"""

from typing import List
from src.frameworks.base import BaseFramework, StepDefinition


class ThreeHorizonsFramework(BaseFramework):
    """Three Horizons of Growth framework by McKinsey & Co."""

    @property
    def name(self) -> str:
        return "Three Horizons of Growth"

    @property
    def description(self) -> str:
        return (
            "Best for managing innovation and growth across three time horizons: "
            "Horizon 1 (core business — defend and extend), Horizon 2 (emerging "
            "opportunities — invest and scale), and Horizon 3 (future possibilities — "
            "explore and experiment). Ideal for corporate strategy, innovation management, "
            "and long-term growth planning. Introduced by McKinsey & Co."
        )

    @property
    def steps(self) -> List[StepDefinition]:
        return [
            StepDefinition(
                index=0,
                name="Analyze Horizon 1 — Core Business",
                description="Assess the current core business: its performance, competitive position, and remaining potential",
                system_prompt=(
                    "You are an expert in the Three Horizons of Growth framework by McKinsey & Co. "
                    "Your task is to analyze Horizon 1 — the core business. "
                    "Horizon 1 represents the current business that generates most of the "
                    "profit and cash flow. Assess: 1) Current revenue and profit performance "
                    "2) Market share and competitive position 3) Remaining growth potential "
                    "4) Key risks and threats to the core 5) Efficiency and optimization "
                    "opportunities 6) How long can the core sustain current performance? "
                    "Be realistic about the core's trajectory."
                ),
                temperature=0.5,
                max_tokens=1536,
            ),
            StepDefinition(
                index=1,
                name="Identify Horizon 2 — Emerging Opportunities",
                description="Identify fast-growing opportunities that could become the next core business",
                system_prompt=(
                    "You are an expert in the Three Horizons of Growth framework by McKinsey & Co. "
                    "You are continuing a growth strategy analysis. "
                    "Identify Horizon 2 opportunities — emerging businesses or initiatives "
                    "that are growing fast and could become the next core. "
                    "These are not yet fully proven but show strong potential. "
                    "Consider: 1) Adjacent market opportunities "
                    "2) New product or service lines gaining traction "
                    "3) New customer segments or channels showing promise "
                    "4) Scalable business models being tested "
                    "5) Competitive threats that could be turned into opportunities "
                    "For each, assess: current traction, growth rate, investment needs, and risk."
                ),
                temperature=0.7,
                max_tokens=2048,
            ),
            StepDefinition(
                index=2,
                name="Explore Horizon 3 — Future Possibilities",
                description="Brainstorm speculative, long-term opportunities that could transform the business in 5-10 years",
                system_prompt=(
                    "You are an expert in the Three Horizons of Growth framework by McKinsey & Co. "
                    "You are continuing a growth strategy analysis. "
                    "Explore Horizon 3 — future possibilities that could transform "
                    "the business in 5-10 years. These are speculative, high-risk, "
                    "but potentially high-reward opportunities. "
                    "Consider: 1) Disruptive technologies and trends "
                    "2) Emerging business models from other industries "
                    "3) 'What if' scenarios that could reshape the market "
                    "4) Adjacent or completely new industries to enter "
                    "5) Platform or ecosystem plays "
                    "6) Bold bets that don't fit current business model "
                    "For each, describe the vision, the signal vs. noise, "
                    "and what would need to be true for it to succeed."
                ),
                temperature=0.8,
                max_tokens=2048,
            ),
            StepDefinition(
                index=3,
                name="Balance the Portfolio Across Horizons",
                description="Allocate resources and attention across the three horizons for optimal growth",
                system_prompt=(
                    "You are an expert in the Three Horizons of Growth framework by McKinsey & Co. "
                    "You are continuing a growth strategy analysis. "
                    "Balance the portfolio across all three horizons. "
                    "Address: 1) Current resource allocation across horizons "
                    "2) Recommended allocation (typical: 70% H1, 20% H2, 10% H3) "
                    "3) Gaps in the current portfolio "
                    "4) How to fund H2 and H3 from H1 cash flow "
                    "5) Metrics and milestones for each horizon "
                    "6) Governance — how to manage different horizons differently "
                    "7) Talent and capability requirements for each horizon "
                    "The goal is a balanced portfolio that sustains current business "
                    "while building future growth engines."
                ),
                temperature=0.5,
                max_tokens=2048,
            ),
            StepDefinition(
                index=4,
                name="Create an Innovation Roadmap",
                description="Develop a phased roadmap with specific initiatives, timelines, and resource commitments",
                system_prompt=(
                    "You are an expert in the Three Horizons of Growth framework by McKinsey & Co. "
                    "You are completing a growth strategy analysis. "
                    "Create a phased innovation roadmap that spans all three horizons. "
                    "For each horizon, define: 1) Specific initiatives and projects "
                    "2) Timeline (H1: now-18 months, H2: 18-36 months, H3: 3-10 years) "
                    "3) Resource requirements (people, capital, technology) "
                    "4) Key milestones and decision gates "
                    "5) Success metrics and KPIs "
                    "6) Risk factors and mitigation strategies "
                    "7) Go/no-go decision criteria for advancing H2→H1 and H3→H2 "
                    "Show how the portfolio evolves over time as initiatives mature."
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
                "Analyze Horizon 1 — the core business. Assess current performance, "
                "competitive position, remaining growth potential, and key risks. "
                "Be realistic about how long the core can sustain current performance."
            )
        elif step_index == 1:
            user_prompt = (
                f"Original context: {question}\n\n"
                f"Horizon 1 analysis (from Step 1):\n{previous_outputs[0]}\n\n"
                "Identify Horizon 2 opportunities — emerging businesses or initiatives "
                "that are growing fast and could become the next core. "
                "For each, assess traction, growth rate, investment needs, and risk."
            )
        elif step_index == 2:
            context = "\n\n".join([
                f"Step {i+1}: {out}"
                for i, out in enumerate(previous_outputs)
            ])
            user_prompt = (
                f"Original context: {question}\n\n"
                f"Previous analysis:\n{context}\n\n"
                "Explore Horizon 3 — future possibilities that could transform "
                "the business in 5-10 years. Think big and speculative. "
                "Consider disruptive trends, emerging models, and bold bets."
            )
        elif step_index == 3:
            context = "\n\n".join([
                f"Step {i+1}: {out}"
                for i, out in enumerate(previous_outputs)
            ])
            user_prompt = (
                f"Original context: {question}\n\n"
                f"Previous analysis:\n{context}\n\n"
                "Balance the portfolio across all three horizons. "
                "Recommend resource allocation, identify gaps, "
                "and define how to manage each horizon differently."
            )
        elif step_index == 4:
            context = "\n\n".join([
                f"Step {i+1}: {out}"
                for i, out in enumerate(previous_outputs)
            ])
            user_prompt = (
                f"Original context: {question}\n\n"
                f"Full analysis:\n{context}\n\n"
                "Create a phased innovation roadmap. Define specific initiatives, "
                "timelines, resources, milestones, and decision gates for each horizon. "
                "Show how the portfolio evolves over time."
            )
        else:
            raise ValueError(f"Invalid step index: {step_index}")

        return step.system_prompt, user_prompt
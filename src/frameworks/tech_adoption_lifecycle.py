"""Technology Adoption Life Cycle Framework.

A framework for understanding how different customer segments adopt
new technology over time, from innovators to laggards, and how to
cross the chasm between early adopters and early majority.
Steps:
1. Segment the adoption curve
2. Position the technology on the curve
3. Cross the chasm strategy
4. Develop segment-specific go-to-market plans
"""

from typing import List
from src.frameworks.base import BaseFramework, StepDefinition


class TechAdoptionLifecycleFramework(BaseFramework):
    """Technology Adoption Life Cycle framework by Geoffrey A. Moore."""

    @property
    def name(self) -> str:
        return "Technology Adoption Life Cycle"

    @property
    def description(self) -> str:
        return (
            "Best for understanding how different customer segments adopt new technology "
            "over time, from innovators to laggards. Focuses on the 'chasm' between "
            "early adopters and early majority that many innovations fail to cross. "
            "Ideal for tech marketing, product launches, and growth strategy. "
            "Introduced by Geoffrey A. Moore (Crossing the Chasm)."
        )

    @property
    def steps(self) -> List[StepDefinition]:
        return [
            StepDefinition(
                index=0,
                name="Segment the Adoption Curve",
                description="Map out the five adopter segments: Innovators, Early Adopters, Early Majority, Late Majority, Laggards",
                system_prompt=(
                    "You are an expert in the Technology Adoption Life Cycle by Geoffrey A. Moore. "
                    "Your task is to map the five adopter segments for the technology or innovation. "
                    "Define: 1) Innovators — technology enthusiasts who chase new products "
                    "2) Early Adopters — visionaries who see strategic potential "
                    "3) Early Majority — pragmatists who want proven solutions "
                    "4) Late Majority — conservatives who wait for standards "
                    "5) Laggards — skeptics who resist until necessary. "
                    "Describe each segment's characteristics, motivations, and buying criteria."
                ),
                temperature=0.5,
                max_tokens=1536,
            ),
            StepDefinition(
                index=1,
                name="Position the Technology on the Curve",
                description="Identify where the technology currently sits on the adoption curve and which segments are engaged",
                system_prompt=(
                    "You are an expert in the Technology Adoption Life Cycle by Geoffrey A. Moore. "
                    "You are continuing an adoption analysis. "
                    "Analyze where the technology currently sits on the adoption curve. "
                    "Which segments have been reached? Which are the current customers? "
                    "Where is the mainstream market? Identify if the technology "
                    "is before, at, or past the 'chasm' — the critical gap between "
                    "early adopters and early majority where most innovations fail."
                ),
                temperature=0.7,
                max_tokens=1536,
            ),
            StepDefinition(
                index=2,
                name="Develop the Crossing-the-Chasm Strategy",
                description="Create a strategy to cross from early adopters to the early majority market",
                system_prompt=(
                    "You are an expert in the Technology Adoption Life Cycle by Geoffrey A. Moore. "
                    "You are continuing an adoption analysis. "
                    "Develop a strategy to cross the chasm. The key insight: "
                    "focus on a single, specific beachhead market segment "
                    "where you can achieve a 'whole product' solution. "
                    "Address: 1) Which specific niche market to target first? "
                    "2) What constitutes the 'whole product' for that niche? "
                    "3) What partnerships are needed to complete the solution? "
                    "4) What competitive positioning will dominate that niche? "
                    "5) What distribution channels reach this niche effectively?"
                ),
                temperature=0.7,
                max_tokens=2048,
            ),
            StepDefinition(
                index=3,
                name="Develop Segment-Specific Go-to-Market Plans",
                description="Tailor messaging, positioning, and channels for each adoption segment from mainstream to laggards",
                system_prompt=(
                    "You are an expert in the Technology Adoption Life Cycle by Geoffrey A. Moore. "
                    "You are completing an adoption analysis. "
                    "After crossing the chasm, develop go-to-market plans for each segment: "
                    "1) Early Majority — focus on pragmatism, proven ROI, industry references "
                    "2) Late Majority — focus on standards, support, reliability "
                    "3) Laggards — focus on necessity, forced migration paths "
                    "For each segment, define: messaging, positioning, pricing, "
                    "distribution channels, and sales approach. "
                    "Show how to evolve the offering as you move across segments."
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
                "Map the five adopter segments for this technology or innovation. "
                "For each segment (Innovators, Early Adopters, Early Majority, "
                "Late Majority, Laggards), describe their characteristics, "
                "motivations, and buying criteria in this specific context."
            )
        elif step_index == 1:
            user_prompt = (
                f"Original context: {question}\n\n"
                f"Adopter segments (from Step 1):\n{previous_outputs[0]}\n\n"
                "Where does this technology currently sit on the adoption curve? "
                "Which segments have adopted it? Is it before, at, or past the chasm? "
                "What evidence supports this assessment?"
            )
        elif step_index == 2:
            context = "\n\n".join([
                f"Step {i+1}: {out}"
                for i, out in enumerate(previous_outputs)
            ])
            user_prompt = (
                f"Original context: {question}\n\n"
                f"Previous analysis:\n{context}\n\n"
                "Develop a strategy to cross the chasm. Focus on a specific beachhead "
                "niche, define the whole product, identify partnerships needed, "
                "and plan how to dominate that niche before expanding."
            )
        elif step_index == 3:
            context = "\n\n".join([
                f"Step {i+1}: {out}"
                for i, out in enumerate(previous_outputs)
            ])
            user_prompt = (
                f"Original context: {question}\n\n"
                f"Full analysis:\n{context}\n\n"
                "Develop go-to-market plans for each mainstream segment. "
                "Tailor messaging, positioning, pricing, and channels "
                "for Early Majority, Late Majority, and Laggards. "
                "Show how the offering evolves across segments."
            )
        else:
            raise ValueError(f"Invalid step index: {step_index}")

        return step.system_prompt, user_prompt
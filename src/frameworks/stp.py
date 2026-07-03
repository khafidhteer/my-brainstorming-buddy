"""STP (Segmentation, Targeting, Positioning) Framework.

A classic marketing framework for dividing a market into segments,
selecting the most attractive segments to target, and developing
a positioning strategy for each target segment.
Steps:
1. Market segmentation
2. Evaluate and select target segments
3. Develop positioning strategy
4. Create marketing mix for each segment
"""

from typing import List
from src.frameworks.base import BaseFramework, StepDefinition


class STPFramework(BaseFramework):
    """STP (Segmentation, Targeting, Positioning) framework for marketing strategy."""

    @property
    def name(self) -> str:
        return "STP (Segmentation, Targeting, Positioning)"

    @property
    def description(self) -> str:
        return (
            "Best for dividing a market into distinct segments, selecting the most "
            "attractive segments to target, and developing a positioning strategy "
            "for each target segment. The foundation of modern marketing strategy. "
            "Ideal for go-to-market planning, brand strategy, and marketing campaigns. "
            "Introduced by Philip Kotler, Al Ries, and Jack Trout."
        )

    @property
    def steps(self) -> List[StepDefinition]:
        return [
            StepDefinition(
                index=0,
                name="Market Segmentation",
                description="Divide the market into distinct, meaningful segments based on relevant criteria",
                system_prompt=(
                    "You are an expert in STP (Segmentation, Targeting, Positioning) "
                    "marketing strategy. Your task is to segment the market. "
                    "Use relevant segmentation bases: "
                    "1) Geographic — region, city, climate "
                    "2) Demographic — age, income, education, occupation "
                    "3) Psychographic — lifestyle, values, personality "
                    "4) Behavioral — usage rate, loyalty, benefits sought "
                    "5) Firmographic (for B2B) — industry, size, revenue "
                    "Define 3-5 distinct, measurable, accessible, and actionable segments."
                ),
                temperature=0.7,
                max_tokens=1536,
            ),
            StepDefinition(
                index=1,
                name="Evaluate and Select Target Segments",
                description="Evaluate each segment's attractiveness and select which ones to target",
                system_prompt=(
                    "You are an expert in STP (Segmentation, Targeting, Positioning) "
                    "marketing strategy. You are continuing a marketing analysis. "
                    "Evaluate each segment's attractiveness: "
                    "1) Size and growth potential "
                    "2) Segment profitability and margins "
                    "3) Competitive intensity within the segment "
                    "4) Accessibility and reachability "
                    "5) Alignment with company capabilities and resources "
                    "6) Strategic fit with company vision "
                    "Score each segment and recommend which to target. "
                    "Specify the targeting strategy: undifferentiated, differentiated, "
                    "concentrated, or micromarketing."
                ),
                temperature=0.5,
                max_tokens=2048,
            ),
            StepDefinition(
                index=2,
                name="Develop Positioning Strategy",
                description="Create a compelling position for your offering in each target segment's mind",
                system_prompt=(
                    "You are an expert in STP (Segmentation, Targeting, Positioning) "
                    "marketing strategy. You are continuing a marketing analysis. "
                    "Develop a positioning strategy for each target segment. "
                    "A positioning statement follows: "
                    "'To [target segment], [brand] is the [category] that [key benefit] "
                    "because [reason to believe].' "
                    "Address: 1) Points of difference vs. competitors "
                    "2) Points of parity (table stakes) "
                    "3) The positioning frame of reference "
                    "4) The brand promise and personality "
                    "5) How the position will be communicated "
                    "Use a positioning map/perceptual map to visualize differentiation."
                ),
                temperature=0.7,
                max_tokens=2048,
            ),
            StepDefinition(
                index=3,
                name="Create Marketing Mix for Each Segment",
                description="Tailor the 4Ps (Product, Price, Place, Promotion) for each target segment",
                system_prompt=(
                    "You are an expert in STP (Segmentation, Targeting, Positioning) "
                    "marketing strategy. You are completing a marketing analysis. "
                    "Create a tailored marketing mix (4Ps) for each target segment: "
                    "1) PRODUCT — features, quality, branding, packaging, variations "
                    "2) PRICE — pricing strategy, discounts, payment terms "
                    "3) PLACE — distribution channels, logistics, coverage "
                    "4) PROMOTION — advertising, PR, sales, digital marketing "
                    "Ensure each mix is consistent with the positioning strategy "
                    "and adapted to the specific segment's needs and preferences. "
                    "Show how the mix differs across segments."
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
                "Segment the market into 3-5 distinct segments. "
                "Use relevant segmentation bases (geographic, demographic, "
                "psychographic, behavioral, or firmographic). "
                "Each segment should be measurable, accessible, and actionable."
            )
        elif step_index == 1:
            user_prompt = (
                f"Original context: {question}\n\n"
                f"Market segments (from Step 1):\n{previous_outputs[0]}\n\n"
                "Evaluate each segment's attractiveness. Consider size, growth, "
                "profitability, competition, accessibility, and strategic fit. "
                "Score each and recommend which segments to target."
            )
        elif step_index == 2:
            context = "\n\n".join([
                f"Step {i+1}: {out}"
                for i, out in enumerate(previous_outputs)
            ])
            user_prompt = (
                f"Original context: {question}\n\n"
                f"Previous analysis:\n{context}\n\n"
                "Develop a positioning strategy for each target segment. "
                "Create positioning statements, identify points of difference, "
                "and explain how the brand will be positioned in each segment's mind."
            )
        elif step_index == 3:
            context = "\n\n".join([
                f"Step {i+1}: {out}"
                for i, out in enumerate(previous_outputs)
            ])
            user_prompt = (
                f"Original context: {question}\n\n"
                f"Full analysis:\n{context}\n\n"
                "Create a tailored marketing mix for each target segment. "
                "Define Product, Price, Place, and Promotion for each, "
                "ensuring consistency with the positioning strategy."
            )
        else:
            raise ValueError(f"Invalid step index: {step_index}")

        return step.system_prompt, user_prompt
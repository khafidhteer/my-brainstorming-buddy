"""Blue Ocean Strategy Framework.

A framework for creating uncontested market space by simultaneously
pursuing differentiation and low cost through the Four Actions Framework
(Eliminate, Reduce, Raise, Create). Steps:
1. Analyze the current strategic profile
2. Apply the Four Actions Framework
3. Develop the strategy canvas
4. Define the new value curve
5. Execute and sustain the blue ocean
"""

from typing import List
from src.frameworks.base import BaseFramework, StepDefinition


class BlueOceanFramework(BaseFramework):
    """Blue Ocean Strategy framework by W. Chan Kim and Renee Mauborgne."""

    @property
    def name(self) -> str:
        return "Blue Ocean Strategy"

    @property
    def description(self) -> str:
        return (
            "Best for creating uncontested market space by simultaneously pursuing "
            "differentiation and low cost. Uses the Four Actions Framework "
            "(Eliminate, Reduce, Raise, Create) and Strategy Canvas. "
            "Ideal for innovation strategy, market creation, and breaking away from competition. "
            "Introduced by Professors W. Chan Kim and Renee Mauborgne (INSEAD)."
        )

    @property
    def steps(self) -> List[StepDefinition]:
        return [
            StepDefinition(
                index=0,
                name="Analyze the Current Strategic Profile",
                description="Map the current competitive landscape and the factors the industry competes on",
                system_prompt=(
                    "You are an expert in Blue Ocean Strategy by Kim and Mauborgne. "
                    "Your task is to analyze the current strategic profile of the industry. "
                    "Map the key competitive factors that the industry currently competes on "
                    "(e.g., price, quality, features, service). "
                    "Identify the 'red ocean' — the crowded, competitive space "
                    "where companies fight for market share."
                ),
                temperature=0.7,
                max_tokens=1536,
            ),
            StepDefinition(
                index=1,
                name="Apply the Four Actions Framework",
                description="Apply Eliminate-Reduce-Raise-Create to break the value-cost trade-off",
                system_prompt=(
                    "You are an expert in Blue Ocean Strategy by Kim and Mauborgne. "
                    "You are continuing a strategy analysis. "
                    "Apply the Four Actions Framework to each competitive factor: "
                    "1) ELIMINATE — Which factors the industry has long competed on should be eliminated? "
                    "2) REDUCE — Which factors should be reduced well below industry standard? "
                    "3) RAISE — Which factors should be raised well above industry standard? "
                    "4) CREATE — Which factors should be created that the industry has never offered? "
                    "This breaks the value-cost trade-off."
                ),
                temperature=0.7,
                max_tokens=2048,
            ),
            StepDefinition(
                index=2,
                name="Develop the Strategy Canvas",
                description="Create a visual strategy canvas comparing the current industry and your new strategy",
                system_prompt=(
                    "You are an expert in Blue Ocean Strategy by Kim and Mauborgne. "
                    "You are continuing a strategy analysis. "
                    "Develop a Strategy Canvas — a visual framework comparing: "
                    "1) The current industry value curve (how competitors perform on key factors) "
                    "2) Your new value curve based on the Four Actions "
                    "Show clearly how your strategy diverges from the industry. "
                    "The goal is a value curve that stands apart — lower on some factors, "
                    "higher on others, and introducing new factors entirely."
                ),
                temperature=0.5,
                max_tokens=2048,
            ),
            StepDefinition(
                index=3,
                name="Define the New Value Curve",
                description="Articulate the new value proposition and the strategic profile of the blue ocean",
                system_prompt=(
                    "You are an expert in Blue Ocean Strategy by Kim and Mauborgne. "
                    "You are continuing a strategy analysis. "
                    "Define the new value curve clearly. Articulate: "
                    "1) The new value proposition — what makes it compelling? "
                    "2) The strategic profile — how does it achieve both differentiation and low cost? "
                    "3) The target audience for this blue ocean offering "
                    "4) The pricing model and revenue mechanics "
                    "5) Why it's difficult for competitors to copy "
                    "Test your strategy against the three criteria: focus, divergence, compelling tagline."
                ),
                temperature=0.7,
                max_tokens=2048,
            ),
            StepDefinition(
                index=4,
                name="Execute and Sustain the Blue Ocean",
                description="Plan the execution, including organizational, operational, and cultural changes needed",
                system_prompt=(
                    "You are an expert in Blue Ocean Strategy by Kim and Mauborgne. "
                    "You are completing a strategy analysis. "
                    "Plan the execution and sustainability of your blue ocean strategy. "
                    "Address: 1) What organizational changes are needed? "
                    "2) What operational processes must change? "
                    "3) What cultural shifts are required? "
                    "4) How to sequence the rollout? "
                    "5) How to defend against imitators? "
                    "6) How to identify and execute the next blue ocean move? "
                    "Consider the four organizational hurdles: cognitive, resource, "
                    "motivational, and political."
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
                "Analyze the current competitive landscape. What are the key factors "
                "the industry competes on? What is the 'red ocean' of competition? "
                "Map the existing strategic profile of the industry."
            )
        elif step_index == 1:
            user_prompt = (
                f"Original context: {question}\n\n"
                f"Current landscape (from Step 1):\n{previous_outputs[0]}\n\n"
                "Apply the Four Actions Framework: For each competitive factor, "
                "decide whether to Eliminate, Reduce, Raise, or Create. "
                "Explain the rationale for each decision."
            )
        elif step_index == 2:
            context = "\n\n".join([
                f"Step {i+1}: {out}"
                for i, out in enumerate(previous_outputs)
            ])
            user_prompt = (
                f"Original context: {question}\n\n"
                f"Previous analysis:\n{context}\n\n"
                "Develop the Strategy Canvas. Compare the industry's current value curve "
                "against your proposed new value curve. Show where you diverge "
                "and how you create a new market space."
            )
        elif step_index == 3:
            context = "\n\n".join([
                f"Step {i+1}: {out}"
                for i, out in enumerate(previous_outputs)
            ])
            user_prompt = (
                f"Original context: {question}\n\n"
                f"Previous analysis:\n{context}\n\n"
                "Define the new value curve. Articulate the value proposition, "
                "strategic profile, target audience, pricing, and competitive defensibility. "
                "Test against the three criteria: focus, divergence, compelling tagline."
            )
        elif step_index == 4:
            context = "\n\n".join([
                f"Step {i+1}: {out}"
                for i, out in enumerate(previous_outputs)
            ])
            user_prompt = (
                f"Original context: {question}\n\n"
                f"Full analysis:\n{context}\n\n"
                "Plan the execution. What organizational, operational, and cultural "
                "changes are needed? How to overcome the four organizational hurdles "
                "(cognitive, resource, motivational, political)? "
                "How to sustain the blue ocean over time?"
            )
        else:
            raise ValueError(f"Invalid step index: {step_index}")

        return step.system_prompt, user_prompt
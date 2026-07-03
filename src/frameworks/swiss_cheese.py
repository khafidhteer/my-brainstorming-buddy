"""The Swiss Cheese Model Framework.

A model for analyzing accidents in layered defense systems,
understanding how multiple failures align to cause incidents.
Steps:
1. Identify the hazard
2. Map defense layers
3. Find latent conditions / holes
4. Recommend improvements to defenses
"""

from typing import List
from src.frameworks.base import BaseFramework, StepDefinition


class SwissCheeseFramework(BaseFramework):
    """Swiss Cheese Model framework for defense-in-depth analysis."""

    @property
    def name(self) -> str:
        return "The Swiss Cheese Model"

    @property
    def description(self) -> str:
        return (
            "Best for analyzing accidents in layered defense systems. "
            "Views defenses as slices of Swiss cheese with holes that "
            "can align to allow hazards to cause harm. "
            "Focuses on both active failures and latent conditions. "
            "Ideal for healthcare, aviation, nuclear, and any domain "
            "with multiple safety barriers."
        )

    @property
    def steps(self) -> List[StepDefinition]:
        return [
            StepDefinition(
                index=0,
                name="Identify the Hazard",
                description="Clearly define the hazard and the potential for harm",
                system_prompt=(
                    "You are an expert in the Swiss Cheese Model of accident causation. "
                    "Start by identifying the hazard clearly. "
                    "A hazard is any condition that has the potential "
                    "to cause harm, loss, or damage. "
                    "What is the specific hazard in this situation?"
                ),
                temperature=0.5,
                max_tokens=1024,
            ),
            StepDefinition(
                index=1,
                name="Map Defense Layers",
                description="Identify all defense layers that should protect against the hazard",
                system_prompt=(
                    "You are an expert in the Swiss Cheese Model of accident causation. "
                    "Map out the layers of defense that are (or should be) "
                    "in place to prevent the hazard from causing harm. "
                    "Defenses can include: physical barriers, "
                    "procedures, training, alarms, automation, "
                    "supervision, regulations, and personal protective equipment. "
                    "List each defense layer and explain its intended function."
                ),
                temperature=0.7,
                max_tokens=2048,
            ),
            StepDefinition(
                index=2,
                name="Find Latent Conditions & Holes",
                description="Identify the holes in each defense layer and the latent conditions that created them",
                system_prompt=(
                    "You are an expert in the Swiss Cheese Model of accident causation. "
                    "For each defense layer, identify the 'holes' - weaknesses, "
                    "gaps, or failures that allowed it to be breached. "
                    "Also identify the latent conditions that created or "
                    "contributed to these holes. Latent conditions are "
                    "underlying factors that exist in the system before "
                    "an accident (e.g., poor design, inadequate training, "
                    "production pressure, organizational culture). "
                    "Explain how the holes aligned to allow the accident trajectory."
                ),
                temperature=0.7,
                max_tokens=2560,
            ),
            StepDefinition(
                index=3,
                name="Recommend Improvements",
                description="Recommend improvements to strengthen defense layers and reduce latent conditions",
                system_prompt=(
                    "You are an expert in the Swiss Cheese Model of accident causation. "
                    "Based on the analysis, recommend improvements to: "
                    "1) Strengthen existing defense layers (reduce hole size/frequency) "
                    "2) Add new defense layers where gaps exist "
                    "3) Address latent conditions at their source "
                    "4) Improve monitoring of defense integrity "
                    "Prioritize recommendations by their ability to "
                    "prevent future accident trajectories."
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
                f"Incident/situation to analyze: {question}\n\n"
                "What is the specific hazard in this situation? "
                "Define what could cause harm or damage."
            )
        elif step_index == 1:
            user_prompt = (
                f"Original question: {question}\n\n"
                f"Hazard (from Step 1):\n{previous_outputs[0]}\n\n"
                "What layers of defense are (or should be) in place "
                "to protect against this hazard? List each layer "
                "and explain its intended protective function."
            )
        elif step_index == 2:
            context = "\n\n".join([
                f"Step {i+1}: {out}"
                for i, out in enumerate(previous_outputs)
            ])
            user_prompt = (
                f"Original question: {question}\n\n"
                f"Analysis so far:\n{context}\n\n"
                "For each defense layer, what are the holes/weaknesses? "
                "What latent conditions created these holes? "
                "How did the holes align to allow the accident?"
            )
        elif step_index == 3:
            context = "\n\n".join([
                f"Step {i+1}: {out}"
                for i, out in enumerate(previous_outputs)
            ])
            user_prompt = (
                f"Original question: {question}\n\n"
                f"Full analysis:\n{context}\n\n"
                "What specific improvements would you recommend? "
                "How would you strengthen defenses, add new layers, "
                "and address latent conditions?"
            )
        else:
            raise ValueError(f"Invalid step index: {step_index}")

        return step.system_prompt, user_prompt
"""STAMP (System-Theoretic Accident Model and Processes) Framework.

A systems-theoretic approach to analyzing accidents in complex
socio-technical systems. Steps:
1. Define the system & hazards
2. Identify safety constraints
3. Analyze control structure flaws
4. Examine process models
5. Generate recommendations
"""

from typing import List
from src.frameworks.base import BaseFramework, StepDefinition


class STAMPFramework(BaseFramework):
    """STAMP framework for safety analysis."""

    @property
    def name(self) -> str:
        return "STAMP (System-Theoretic Accident Model)"

    @property
    def description(self) -> str:
        return (
            "Best for analyzing accidents in complex socio-technical systems. "
            "STAMP views safety as a control problem rather than a failure problem. "
            "Analyzes the system's control structure, safety constraints, "
            "and process models to identify why controls were inadequate. "
            "Ideal for aerospace, healthcare, nuclear, and other safety-critical domains."
        )

    @property
    def steps(self) -> List[StepDefinition]:
        return [
            StepDefinition(
                index=0,
                name="Define System & Hazards",
                description="Define the system boundaries, components, and relevant hazards",
                system_prompt=(
                    "You are an expert in STAMP (System-Theoretic Accident Model "
                    "and Processes) analysis. "
                    "Define the system under analysis: its boundaries, "
                    "key components, and stakeholders. "
                    "Then identify the specific hazards (not just events) "
                    "that represent potential for loss or harm."
                ),
                temperature=0.5,
                max_tokens=1536,
            ),
            StepDefinition(
                index=1,
                name="Identify Safety Constraints",
                description="Identify the safety constraints that should have prevented the hazards",
                system_prompt=(
                    "You are an expert in STAMP analysis. "
                    "For each hazard identified, specify the safety constraints "
                    "that should have been enforced to prevent it. "
                    "Safety constraints are conditions that must be maintained "
                    "for safe operation. Distinguish between: "
                    "1) System-level constraints "
                    "2) Component-level constraints "
                    "3) Interaction constraints between components"
                ),
                temperature=0.7,
                max_tokens=2048,
            ),
            StepDefinition(
                index=2,
                name="Analyze Control Structure Flaws",
                description="Map and analyze the control structure to find why safety constraints were not enforced",
                system_prompt=(
                    "You are an expert in STAMP analysis. "
                    "Map the hierarchical control structure of the system. "
                    "Identify: who or what is providing control, "
                    "what controllers are responsible for each safety constraint, "
                    "what feedback loops exist (or are missing), "
                    "and where control actions were inadequate or missing. "
                    "Look for: missing controllers, inadequate feedback, "
                    "uncontrolled processes, and coordination failures."
                ),
                temperature=0.7,
                max_tokens=2560,
            ),
            StepDefinition(
                index=3,
                name="Examine Process Models",
                description="Analyze how controllers' mental models of the system contributed to the failure",
                system_prompt=(
                    "You are an expert in STAMP analysis. "
                    "Examine the process models (mental models) of each "
                    "controller in the system. A process model is the controller's "
                    "understanding of: the current system state, the desired state, "
                    "and the ways the system can change. "
                    "Identify mismatches between the process model and reality "
                    "that led to unsafe control actions. "
                    "Also consider: what feedback was available vs. what was used?"
                ),
                temperature=0.7,
                max_tokens=2048,
            ),
            StepDefinition(
                index=4,
                name="Generate Recommendations",
                description="Generate recommendations to improve the control structure and safety constraints",
                system_prompt=(
                    "You are an expert in STAMP analysis. "
                    "Synthesize findings into actionable recommendations. "
                    "For each deficiency found in the control structure: "
                    "1) Propose changes to the control structure "
                    "2) Recommend additional safety constraints "
                    "3) Suggest improvements to feedback loops "
                    "4) Identify ways to improve process model accuracy "
                    "Prioritize recommendations by impact on system safety."
                ),
                temperature=0.5,
                max_tokens=2560,
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
                f"System/incident to analyze: {question}\n\n"
                "Define this system: what are its boundaries, components, "
                "and stakeholders? What are the hazards that could lead to loss?"
            )
        elif step_index == 1:
            user_prompt = (
                f"Original question: {question}\n\n"
                f"System & hazards (from Step 1):\n{previous_outputs[0]}\n\n"
                "For each hazard, what safety constraints should have been "
                "in place? Consider system-level, component-level, "
                "and interaction constraints."
            )
        elif step_index == 2:
            context = "\n\n".join([
                f"Step {i+1}: {out}"
                for i, out in enumerate(previous_outputs)
            ])
            user_prompt = (
                f"Original question: {question}\n\n"
                f"Analysis so far:\n{context}\n\n"
                "Map the control structure. Who were the controllers? "
                "What control actions existed? What feedback was available? "
                "Where did control fail?"
            )
        elif step_index == 3:
            context = "\n\n".join([
                f"Step {i+1}: {out}"
                for i, out in enumerate(previous_outputs)
            ])
            user_prompt = (
                f"Original question: {question}\n\n"
                f"Analysis so far:\n{context}\n\n"
                "For each controller, what was their process model "
                "(understanding of system state)? Where was it incorrect? "
                "What feedback was missing or not used?"
            )
        elif step_index == 4:
            context = "\n\n".join([
                f"Step {i+1}: {out}"
                for i, out in enumerate(previous_outputs)
            ])
            user_prompt = (
                f"Original question: {question}\n\n"
                f"Full analysis:\n{context}\n\n"
                "Based on all findings, what are your recommendations "
                "for improving the system's control structure, "
                "safety constraints, feedback loops, and process models?"
            )
        else:
            raise ValueError(f"Invalid step index: {step_index}")

        return step.system_prompt, user_prompt
"""DMAIC Framework (Define, Measure, Analyze, Improve, Control).

A data-driven quality improvement methodology used in Six Sigma.
Steps:
1. Define - Problem statement, goals, scope
2. Measure - Key metrics, baseline data
3. Analyze - Root cause analysis
4. Improve - Solutions, implementation
5. Control - Monitoring plan, sustainment
"""

from typing import List
from src.frameworks.base import BaseFramework, StepDefinition


class DMAICFramework(BaseFramework):
    """DMAIC framework for process improvement."""

    @property
    def name(self) -> str:
        return "DMAIC (Define-Measure-Analyze-Improve-Control)"

    @property
    def description(self) -> str:
        return (
            "Best for process improvement, quality control, and "
            "business optimization. A data-driven five-phase methodology: "
            "Define the problem and goals, Measure current performance, "
            "Analyze root causes, Improve the process, Control to sustain gains. "
            "Ideal for manufacturing, service, and business process improvement."
        )

    @property
    def steps(self) -> List[StepDefinition]:
        return [
            StepDefinition(
                index=0,
                name="Define",
                description="Define the problem, project goals, scope, and customer requirements",
                system_prompt=(
                    "You are an expert in DMAIC (Six Sigma) process improvement. "
                    "Phase 1: DEFINE. "
                    "Clearly define: the problem, project goals, scope, "
                    "customer requirements, and key stakeholders. "
                    "Use a problem statement format: "
                    "'[Problem] is affecting [impact], resulting in [consequences]. "
                    "Success would look like [target state].'"
                ),
                temperature=0.5,
                max_tokens=1536,
            ),
            StepDefinition(
                index=1,
                name="Measure",
                description="Measure current process performance and establish baseline",
                system_prompt=(
                    "You are an expert in DMAIC (Six Sigma) process improvement. "
                    "Phase 2: MEASURE. "
                    "Define: key metrics (KPIs), data collection methods, "
                    "current baseline performance, and target performance levels. "
                    "Consider: what would you measure to understand the current state? "
                    "What data exists and what needs to be collected? "
                    "Establish a baseline for the metric(s) of interest."
                ),
                temperature=0.7,
                max_tokens=2048,
            ),
            StepDefinition(
                index=2,
                name="Analyze",
                description="Analyze data to identify root causes of the problem",
                system_prompt=(
                    "You are an expert in DMAIC (Six Sigma) process improvement. "
                    "Phase 3: ANALYZE. "
                    "Analyze the data and process to identify root causes. "
                    "Use: process mapping, value stream analysis, "
                    "cause-effect analysis, hypothesis testing, "
                    "or any relevant analytical methods. "
                    "Identify the vital few X's (input variables) "
                    "that drive the Y (output/outcome). "
                    "Prioritize root causes by their impact."
                ),
                temperature=0.7,
                max_tokens=2560,
            ),
            StepDefinition(
                index=3,
                name="Improve",
                description="Develop and implement solutions to address root causes",
                system_prompt=(
                    "You are an expert in DMAIC (Six Sigma) process improvement. "
                    "Phase 4: IMPROVE. "
                    "Develop solutions for the root causes identified. "
                    "Use techniques like: brainstorming, design of experiments, "
                    "solution selection matrix, pilot testing. "
                    "For each solution: describe it, expected impact, "
                    "implementation effort, and risk. "
                    "Select the best solutions and create an implementation plan."
                ),
                temperature=0.7,
                max_tokens=2560,
            ),
            StepDefinition(
                index=4,
                name="Control",
                description="Establish controls to sustain the improvements",
                system_prompt=(
                    "You are an expert in DMAIC (Six Sigma) process improvement. "
                    "Phase 5: CONTROL. "
                    "Establish controls to sustain the improvements. "
                    "Include: process control plan, monitoring system, "
                    "response plan for deviations, documentation, "
                    "training plan, and handover procedures. "
                    "Also define: how will results be measured over time? "
                    "What are the triggers for corrective action? "
                    "How will the solution be institutionalized?"
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
                f"Process/situation to improve: {question}\n\n"
                "DEFINE phase: Create a clear problem statement. "
                "What is the specific problem? Who are the customers? "
                "What is the scope? What are the goals and targets?"
            )
        elif step_index == 1:
            user_prompt = (
                f"Original question: {question}\n\n"
                f"Definition (from Step 1):\n{previous_outputs[0]}\n\n"
                "MEASURE phase: What key metrics would measure current performance? "
                "What is the baseline? What data is needed? "
                "What is the target performance level?"
            )
        elif step_index == 2:
            context = "\n\n".join([
                f"Step {i+1}: {out}"
                for i, out in enumerate(previous_outputs)
            ])
            user_prompt = (
                f"Original question: {question}\n\n"
                f"Analysis so far:\n{context}\n\n"
                "ANALYZE phase: What are the root causes? "
                "Use appropriate analytical methods. "
                "Identify the vital few X's driving the Y."
            )
        elif step_index == 3:
            context = "\n\n".join([
                f"Step {i+1}: {out}"
                for i, out in enumerate(previous_outputs)
            ])
            user_prompt = (
                f"Original question: {question}\n\n"
                f"Analysis so far:\n{context}\n\n"
                "IMPROVE phase: What solutions address the root causes? "
                "Describe each solution, expected impact, and effort required. "
                "Select the best solutions and outline implementation."
            )
        elif step_index == 4:
            context = "\n\n".join([
                f"Step {i+1}: {out}"
                for i, out in enumerate(previous_outputs)
            ])
            user_prompt = (
                f"Original question: {question}\n\n"
                f"Full analysis:\n{context}\n\n"
                "CONTROL phase: How will improvements be sustained? "
                "Define monitoring plan, response procedures, "
                "training needs, and documentation."
            )
        else:
            raise ValueError(f"Invalid step index: {step_index}")

        return step.system_prompt, user_prompt
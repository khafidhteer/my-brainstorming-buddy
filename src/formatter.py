"""Output formatting for framework reasoning chains.

Formats the reasoning chain results for both CLI and Streamlit display.
"""

from typing import List, Dict, Any
import json


class StepOutput:
    """Represents the output of a single step in the chain."""

    def __init__(
        self,
        step_index: int,
        step_name: str,
        step_description: str,
        prompt: str,
        output: str,
    ):
        self.step_index = step_index
        self.step_name = step_name
        self.step_description = step_description
        self.prompt = prompt
        self.output = output

    def to_dict(self) -> Dict[str, Any]:
        return {
            "step": self.step_index + 1,
            "name": self.step_name,
            "description": self.step_description,
            "output": self.output,
        }


class ChainResult:
    """Complete result of a framework reasoning chain."""

    def __init__(
        self,
        question: str,
        framework_name: str,
        framework_description: str,
        steps: List[StepOutput],
        total_steps: int,
        framework_key: str,
    ):
        self.question = question
        self.framework_name = framework_name
        self.framework_description = framework_description
        self.steps = steps
        self.total_steps = total_steps
        self.framework_key = framework_key

    def to_dict(self) -> Dict[str, Any]:
        return {
            "question": self.question,
            "framework": {
                "name": self.framework_name,
                "description": self.framework_description,
                "key": self.framework_key,
            },
            "steps": [s.to_dict() for s in self.steps],
            "total_steps": self.total_steps,
        }

    def to_json(self, indent: int = 2) -> str:
        """Serialize to JSON string."""
        return json.dumps(self.to_dict(), indent=indent)

    def to_markdown(self) -> str:
        """Format as a readable Markdown string."""
        lines: List[str] = []
        lines.append(f"# Chain-of-Thought Analysis")
        lines.append("")
        lines.append(f"**Question:** {self.question}")
        lines.append("")
        lines.append(
            f"**Framework:** {self.framework_name} "
            f"({self.framework_key})"
        )
        lines.append("")
        lines.append(f"_{self.framework_description}_")
        lines.append("")
        lines.append("---")
        lines.append("")

        for step in self.steps:
            lines.append(f"## Step {step.step_index + 1}: {step.step_name}")
            lines.append("")
            lines.append(f"_{step.step_description}_")
            lines.append("")
            lines.append(step.output)
            lines.append("")
            lines.append("---")
            lines.append("")

        lines.append("## Summary")
        lines.append("")
        lines.append(
            f"Completed {len(self.steps)} of {self.total_steps} steps "
            f"using the **{self.framework_name}** framework."
        )
        lines.append("")

        return "\n".join(lines)

    def to_text(self) -> str:
        """Format as plain text."""
        lines: List[str] = []
        lines.append("=" * 60)
        lines.append("CHAIN-OF-THOUGHT ANALYSIS")
        lines.append("=" * 60)
        lines.append(f"Question: {self.question}")
        lines.append(f"Framework: {self.framework_name}")
        lines.append(f"Description: {self.framework_description}")
        lines.append("-" * 60)

        for step in self.steps:
            lines.append("")
            lines.append(
                f"Step {step.step_index + 1}: {step.step_name}"
            )
            lines.append(f"  {step.step_description}")
            lines.append("")
            lines.append(step.output)
            lines.append("")
            lines.append("-" * 40)

        lines.append("")
        lines.append(
            f"Completed {len(self.steps)}/{self.total_steps} steps "
            f"using {self.framework_name}."
        )
        lines.append("=" * 60)

        return "\n".join(lines)
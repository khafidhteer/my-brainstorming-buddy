"""Base framework class for all Chain-of-Thought frameworks.

All frameworks must inherit from BaseFramework and implement
the required properties and methods.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class StepDefinition:
    """Defines a single step in a framework's reasoning chain."""

    def __init__(
        self,
        index: int,
        name: str,
        description: str,
        system_prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ):
        self.index = index
        self.name = name
        self.description = description
        self.system_prompt = system_prompt
        self.temperature = temperature
        self.max_tokens = max_tokens

    def to_dict(self) -> Dict[str, Any]:
        """Convert step definition to dictionary."""
        return {
            "index": self.index,
            "name": self.name,
            "description": self.description,
        }


class BaseFramework(ABC):
    """Abstract base class for all frameworks."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable framework name."""
        ...

    @property
    @abstractmethod
    def description(self) -> str:
        """Description of what this framework is good for."""
        ...

    @property
    @abstractmethod
    def steps(self) -> List[StepDefinition]:
        """Ordered list of steps in this framework's chain."""
        ...

    @abstractmethod
    def generate_prompt(
        self,
        step_index: int,
        question: str,
        previous_outputs: List[str],
    ) -> tuple[str, str]:
        """Generate the (system_prompt, user_prompt) for a given step.

        Args:
            step_index: The index of the current step.
            question: The original user question.
            previous_outputs: List of LLM outputs from previous steps.

        Returns:
            Tuple of (system_prompt, user_prompt) for this step.
        """
        ...

    def should_terminate(
        self,
        step_index: int,
        output: str,
    ) -> bool:
        """Determine if the chain should stop early.

        Override this in subclasses to implement early termination logic.

        Args:
            step_index: The index of the step that just completed.
            output: The LLM output from this step.

        Returns:
            True if the chain should terminate early.
        """
        return False

    def get_step(self, step_index: int) -> Optional[StepDefinition]:
        """Get step definition by index."""
        if 0 <= step_index < len(self.steps):
            return self.steps[step_index]
        return None

    @property
    def total_steps(self) -> int:
        """Total number of steps in this framework."""
        return len(self.steps)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize framework info to dictionary."""
        return {
            "name": self.name,
            "description": self.description,
            "steps": [s.to_dict() for s in self.steps],
            "total_steps": self.total_steps,
        }
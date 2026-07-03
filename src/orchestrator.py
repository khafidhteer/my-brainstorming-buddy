"""Chain-of-Thought Orchestrator Engine.

Manages the execution of framework reasoning chains, calling the LLM
at each step and passing context forward.
"""

import logging
from typing import List, Optional

from src.frameworks.base import BaseFramework
from src.llm_adapter import LLMAdapter
from src.formatter import StepOutput, ChainResult
from src.framework_selector import select_framework, list_frameworks

logger = logging.getLogger(__name__)


class Orchestrator:
    """Orchestrates the chain-of-thought reasoning process."""

    def __init__(self, llm_adapter: LLMAdapter):
        self.llm = llm_adapter

    async def analyze(
        self,
        question: str,
        preferred_framework: Optional[str] = None,
        verbose: bool = False,
    ) -> ChainResult:
        """Run a complete analysis chain on a question.

        Args:
            question: The user's question to analyze.
            preferred_framework: Optional framework override (by key name).
            verbose: If True, log detailed step information.

        Returns:
            ChainResult containing all steps and outputs.
        """
        # Step 1: Select the best framework
        framework, framework_key = await select_framework(
            question=question,
            llm_adapter=self.llm,
            preferred=preferred_framework,
        )

        if verbose:
            logger.info(f"Selected framework: {framework.name} ({framework_key})")
            logger.info(f"Total steps: {framework.total_steps}")

        steps: List[StepOutput] = []
        previous_outputs: List[str] = []

        # Step 2: Execute each step in the chain
        for step_index in range(framework.total_steps):
            step_def = framework.get_step(step_index)
            if not step_def:
                logger.warning(f"No step definition for index {step_index}, skipping")
                continue

            # Check if we should terminate early
            if framework.should_terminate(step_index, previous_outputs):
                if verbose:
                    logger.info(f"Early termination at step {step_index + 1}")
                break

            # Generate prompts for this step
            system_prompt, user_prompt = framework.generate_prompt(
                step_index=step_index,
                question=question,
                previous_outputs=previous_outputs,
            )

            if verbose:
                logger.info(f"Executing step {step_index + 1}: {step_def.name}")

            # Call the LLM
            output = await self.llm.chat_completion(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                temperature=step_def.temperature,
                max_tokens=step_def.max_tokens,
            )

            # Record the step output
            step_output = StepOutput(
                step_index=step_index,
                step_name=step_def.name,
                step_description=step_def.description,
                prompt=user_prompt,
                output=output,
            )
            steps.append(step_output)
            previous_outputs.append(output)

        # Step 3: Return the complete chain result
        return ChainResult(
            question=question,
            framework_name=framework.name,
            framework_description=framework.description,
            steps=steps,
            total_steps=framework.total_steps,
            framework_key=framework_key,
        )

    def get_available_frameworks(self) -> list[dict]:
        """Get list of all available frameworks."""
        return list_frameworks()
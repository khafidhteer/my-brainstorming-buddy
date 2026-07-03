"""Framework selector for automatic framework detection.

Uses the LLM to classify which framework best suits a given question.
"""

import logging
from typing import Optional

from src.frameworks import (
    BaseFramework,
    FishboneFramework,
    FaultTreeFramework,
    IcebergFramework,
    ApolloRCAFramework,
    STAMPFramework,
    SwissCheeseFramework,
    CynefinFramework,
    DMAICFramework,
)

logger = logging.getLogger(__name__)

# Registry of all available frameworks
FRAMEWORK_REGISTRY: dict[str, type[BaseFramework]] = {
    "fishbone": FishboneFramework,
    "fault_tree": FaultTreeFramework,
    "iceberg": IcebergFramework,
    "apollo_rca": ApolloRCAFramework,
    "stamp": STAMPFramework,
    "swiss_cheese": SwissCheeseFramework,
    "cynefin": CynefinFramework,
    "dmaic": DMAICFramework,
}

# Framework classification prompt
CLASSIFICATION_PROMPT = """You are an expert in analytical frameworks. Given a user's question, 
determine which of these frameworks would be BEST suited to analyze it.

Available frameworks:
1. fishbone - Fishbone Diagram (Ishikawa): Best for identifying multiple root causes of a problem, especially in manufacturing, engineering, and business processes. Good for "why did this happen?" questions.
2. fault_tree - Fault Tree Analysis: Best for analyzing system failures and safety incidents using deductive logic (OR/AND gates). Good for "what could cause this failure?" questions.
3. iceberg - Iceberg Model: Best for understanding deep systemic issues beyond surface events. Good for "what's really going on beneath the surface?" questions.
4. apollo_rca - Apollo Root Cause Analysis: Best for thorough investigation of incidents with a focus on causal relationships. Good for "what caused this incident?" questions.
5. stamp - STAMP (System-Theoretic Accident Model): Best for analyzing complex socio-technical systems, safety-critical systems, and control-related failures.
6. swiss_cheese - Swiss Cheese Model: Best for analyzing accidents in layered defense systems, understanding how multiple failures align to cause incidents.
7. cynefin - Cynefin Framework: Best for classifying the nature of a problem (simple/complicated/complex/chaotic) to determine the appropriate decision-making approach.
8. dmaic - DMAIC (Define-Measure-Analyze-Improve-Control): Best for process improvement, quality control, Six Sigma projects, and business optimization questions.

Respond with ONLY a JSON object:
{
  "framework": "framework_name",
  "confidence": 0.0-1.0,
  "reasoning": "One sentence explaining why this framework fits"
}

Use the framework name exactly as listed above."""


async def select_framework(
    question: str,
    llm_adapter,
    preferred: Optional[str] = None,
) -> tuple[BaseFramework, str]:
    """Select the best framework for a given question.

    Args:
        question: The user's question.
        llm_adapter: LLMAdapter instance for classification.
        preferred: Optional framework override (by name).

    Returns:
        Tuple of (framework_instance, framework_key).

    Raises:
        ValueError: If preferred framework is not found.
    """
    # Manual override
    if preferred:
        preferred = preferred.lower().replace(" ", "_")
        if preferred in FRAMEWORK_REGISTRY:
            framework_class = FRAMEWORK_REGISTRY[preferred]
            return framework_class(), preferred
        raise ValueError(
            f"Framework '{preferred}' not found. "
            f"Available: {', '.join(FRAMEWORK_REGISTRY.keys())}"
        )

    # Auto-detect using LLM
    try:
        result = await llm_adapter.structured_completion(
            system_prompt=CLASSIFICATION_PROMPT,
            user_prompt=f"Question: {question}\n\nWhich framework is best?",
            max_tokens=512,
        )

        framework_key = result.get("framework", "fishbone").lower().replace(" ", "_")
        confidence = result.get("confidence", 0.0)

        logger.info(
            f"Auto-selected framework: {framework_key} "
            f"(confidence: {confidence:.2f})"
        )

        # Fallback to fishbone if unknown framework returned
        if framework_key not in FRAMEWORK_REGISTRY:
            logger.warning(
                f"Unknown framework '{framework_key}', falling back to fishbone"
            )
            framework_key = "fishbone"

    except Exception as e:
        logger.error(f"Framework selection failed: {e}, falling back to fishbone")
        framework_key = "fishbone"

    framework_class = FRAMEWORK_REGISTRY[framework_key]
    return framework_class(), framework_key


def list_frameworks() -> list[dict]:
    """List all available frameworks with descriptions."""
    frameworks = []
    for key, cls in FRAMEWORK_REGISTRY.items():
        instance = cls()
        frameworks.append({
            "key": key,
            "name": instance.name,
            "description": instance.description,
        })
    return frameworks
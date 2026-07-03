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
    JTBDFramework,
    ValuePropositionCanvasFramework,
    BeachheadMarketFramework,
    TechAdoptionLifecycleFramework,
    BlueOceanFramework,
    IdealCustomerProfileFramework,
    STPFramework,
    ThreeHorizonsFramework,
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
    "jtbd": JTBDFramework,
    "value_proposition_canvas": ValuePropositionCanvasFramework,
    "beachhead_market": BeachheadMarketFramework,
    "tech_adoption_lifecycle": TechAdoptionLifecycleFramework,
    "blue_ocean": BlueOceanFramework,
    "ideal_customer_profile": IdealCustomerProfileFramework,
    "stp": STPFramework,
    "three_horizons": ThreeHorizonsFramework,
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
9. jtbd - Jobs-to-be-Done (JTBD): Best for understanding what customers are truly trying to accomplish, focusing on functional, emotional, and social dimensions of the job. Good for product innovation and customer research.
10. value_proposition_canvas - Value Proposition Canvas: Best for designing and testing value propositions by mapping customer profiles against value maps. Good for product development and marketing strategy.
11. beachhead_market - Beachhead Market Strategy: Best for identifying a single market to dominate before expanding to adjacent markets. Good for startup strategy and market entry.
12. tech_adoption_lifecycle - Technology Adoption Life Cycle: Best for understanding how different customer segments adopt new technology and how to cross the chasm. Good for tech marketing and product launches.
13. blue_ocean - Blue Ocean Strategy: Best for creating uncontested market space through the Four Actions Framework (Eliminate-Reduce-Raise-Create). Good for innovation and breaking away from competition.
14. ideal_customer_profile - Ideal Customer Profile: Best for defining the perfect customer to target based on firmographic, demographic, behavioral, and needs-based criteria. Good for sales targeting and lead scoring.
15. stp - STP (Segmentation, Targeting, Positioning): Best for dividing markets into segments, selecting targets, and developing positioning. Good for go-to-market planning and brand strategy.
16. three_horizons - Three Horizons of Growth: Best for managing innovation across Horizon 1 (core), Horizon 2 (emerging), and Horizon 3 (future). Good for corporate strategy and long-term growth planning.

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
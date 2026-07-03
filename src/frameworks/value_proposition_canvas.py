"""Value Proposition Canvas Framework.

A framework for designing, testing, and refining value propositions
by mapping customer profiles (pains, gains, jobs) against value maps
(products, pain relievers, gain creators). Steps:
1. Map customer profile (jobs, pains, gains)
2. Map value map (products, pain relievers, gain creators)
3. Analyze fit between customer profile and value map
4. Prototype and test value proposition
"""

from typing import List
from src.frameworks.base import BaseFramework, StepDefinition


class ValuePropositionCanvasFramework(BaseFramework):
    """Value Proposition Canvas framework for designing customer value."""

    @property
    def name(self) -> str:
        return "Value Proposition Canvas"

    @property
    def description(self) -> str:
        return (
            "Best for designing, testing, and refining value propositions. "
            "Maps customer profiles (jobs, pains, gains) against value maps "
            "(products, pain relievers, gain creators) to achieve fit. "
            "Ideal for product development, marketing strategy, and business model design. "
            "Introduced by Dr. Alexander Osterwalder."
        )

    @property
    def steps(self) -> List[StepDefinition]:
        return [
            StepDefinition(
                index=0,
                name="Map Customer Profile - Jobs",
                description="Identify the functional, social, and emotional jobs your customers are trying to get done",
                system_prompt=(
                    "You are an expert in the Value Proposition Canvas by Alexander Osterwalder. "
                    "Your task is to map the customer profile. "
                    "Identify all the jobs your customers are trying to get done — "
                    "functional jobs (tasks to complete), social jobs (how they want to be perceived), "
                    "and emotional jobs (how they want to feel)."
                ),
                temperature=0.5,
                max_tokens=1024,
            ),
            StepDefinition(
                index=1,
                name="Map Customer Profile - Pains and Gains",
                description="Identify customer pains (negative outcomes, risks, obstacles) and gains (desired outcomes, benefits)",
                system_prompt=(
                    "You are an expert in the Value Proposition Canvas by Alexander Osterwalder. "
                    "You are continuing a customer profile analysis. "
                    "Identify customer pains: negative emotions, undesired outcomes, risks, "
                    "and obstacles related to getting the job done. "
                    "Then identify customer gains: desired outcomes, concrete benefits, "
                    "and positive emotions they seek. Be specific and detailed."
                ),
                temperature=0.7,
                max_tokens=1536,
            ),
            StepDefinition(
                index=2,
                name="Map Value Map - Products and Services",
                description="List the products, services, and offerings that help customers get their jobs done",
                system_prompt=(
                    "You are an expert in the Value Proposition Canvas by Alexander Osterwalder. "
                    "You are continuing a value proposition analysis. "
                    "Now map the value map side. List all the products, services, "
                    "and offerings that could help customers get their jobs done. "
                    "Be comprehensive — include both tangible offerings and intangible benefits. "
                    "Consider the full customer experience."
                ),
                temperature=0.7,
                max_tokens=1536,
            ),
            StepDefinition(
                index=3,
                name="Map Value Map - Pain Relievers and Gain Creators",
                description="Describe how your offerings alleviate pains and create gains for customers",
                system_prompt=(
                    "You are an expert in the Value Proposition Canvas by Alexander Osterwalder. "
                    "You are continuing a value proposition analysis. "
                    "For each offering identified, describe: "
                    "1) Pain relievers — how does it alleviate specific customer pains? "
                    "2) Gain creators — how does it create specific customer gains? "
                    "Be specific about the mechanisms and outcomes."
                ),
                temperature=0.7,
                max_tokens=2048,
            ),
            StepDefinition(
                index=4,
                name="Analyze Fit and Next Steps",
                description="Evaluate the alignment between customer profile and value map, identify gaps and opportunities",
                system_prompt=(
                    "You are an expert in the Value Proposition Canvas by Alexander Osterwalder. "
                    "You are completing a value proposition analysis. "
                    "Analyze the fit between the customer profile and value map. "
                    "Address: 1) Which pains are addressed well vs. not addressed? "
                    "2) Which gains are well-served vs. missed opportunities? "
                    "3) Which jobs have the best solution fit? "
                    "4) What are the critical gaps and how to close them? "
                    "5) What should be tested or validated next? "
                    "6) Provide a clear value proposition statement based on your analysis."
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
                "Map the customer profile by identifying all the jobs "
                "(functional, social, and emotional) that customers are "
                "trying to get done in this context. "
                "What tasks are they trying to complete? "
                "How do they want to be perceived? "
                "How do they want to feel?"
            )
        elif step_index == 1:
            user_prompt = (
                f"Original context: {question}\n\n"
                f"Customer jobs (from Step 1):\n{previous_outputs[0]}\n\n"
                "Now identify the pains and gains: "
                "What negative outcomes, risks, and obstacles do customers face? "
                "What desired outcomes, benefits, and positive experiences do they seek? "
                "Be specific and prioritize the most intense pains and most relevant gains."
            )
        elif step_index == 2:
            context = "\n\n".join([
                f"Step {i+1}: {out}"
                for i, out in enumerate(previous_outputs)
            ])
            user_prompt = (
                f"Original context: {question}\n\n"
                f"Customer profile so far:\n{context}\n\n"
                "Now map the value proposition side. What products, services, "
                "and offerings could address these customer needs? "
                "Be comprehensive — list all potential value elements, "
                "including both core offerings and supplementary services."
            )
        elif step_index == 3:
            context = "\n\n".join([
                f"Step {i+1}: {out}"
                for i, out in enumerate(previous_outputs)
            ])
            user_prompt = (
                f"Original context: {question}\n\n"
                f"Analysis so far:\n{context}\n\n"
                "For each offering, describe how it relieves specific pains "
                "and creates specific gains. Match each pain reliever and "
                "gain creator to the specific pain or gain it addresses."
            )
        elif step_index == 4:
            context = "\n\n".join([
                f"Step {i+1}: {out}"
                for i, out in enumerate(previous_outputs)
            ])
            user_prompt = (
                f"Original context: {question}\n\n"
                f"Full analysis:\n{context}\n\n"
                "Based on all the above, evaluate the fit. "
                "What are the strongest alignments? What gaps exist? "
                "What should be tested or validated? "
                "Provide a clear value proposition statement "
                "and actionable next steps."
            )
        else:
            raise ValueError(f"Invalid step index: {step_index}")

        return step.system_prompt, user_prompt
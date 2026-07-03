"""Jobs-to-be-Done (JTBD) Framework.

A framework for understanding what customers are trying to accomplish
in a given situation, focusing on the functional, emotional, and social
dimensions of the job. Steps:
1. Define the job to be done
2. Identify functional needs
3. Identify emotional needs
4. Identify social needs
5. Synthesize value proposition
"""

from typing import List
from src.frameworks.base import BaseFramework, StepDefinition


class JTBDFramework(BaseFramework):
    """Jobs-to-be-Done framework for customer-centric innovation."""

    @property
    def name(self) -> str:
        return "Jobs-to-be-Done (JTBD)"

    @property
    def description(self) -> str:
        return (
            "Best for understanding what customers are truly trying to accomplish "
            "in a given situation. Focuses on functional, emotional, and social "
            "dimensions of the 'job' customers hire products to do. "
            "Ideal for product innovation, market positioning, and customer research. "
            "Introduced by Clayton Christensen, Tony Ulwick, and Bob Moesta."
        )

    @property
    def steps(self) -> List[StepDefinition]:
        return [
            StepDefinition(
                index=0,
                name="Define the Job to Be Done",
                description="Clearly articulate the core job the customer is trying to accomplish",
                system_prompt=(
                    "You are an expert in Jobs-to-be-Done (JTBD) theory. "
                    "Your task is to help define the customer's core functional job. "
                    "Focus on the progress the customer wants to make in a specific circumstance. "
                    "A good job statement follows: 'When [situation], I want to [motivation] "
                    "so I can [desired outcome].'"
                ),
                temperature=0.5,
                max_tokens=1024,
            ),
            StepDefinition(
                index=1,
                name="Identify Functional Needs",
                description="Identify the functional requirements and desired outcomes for the job",
                system_prompt=(
                    "You are an expert in Jobs-to-be-Done (JTBD) theory. "
                    "You are continuing a JTBD analysis. "
                    "Identify the functional needs — the practical, objective requirements "
                    "the customer has for getting the job done. What metrics define success? "
                    "What functional criteria must be met? Focus on measurable outcomes."
                ),
                temperature=0.7,
                max_tokens=1536,
            ),
            StepDefinition(
                index=2,
                name="Identify Emotional Needs",
                description="Uncover the emotional needs and feelings the customer wants to achieve or avoid",
                system_prompt=(
                    "You are an expert in Jobs-to-be-Done (JTBD) theory. "
                    "You are continuing a JTBD analysis. "
                    "Identify the emotional needs — how the customer wants to feel "
                    "during and after getting the job done. What anxieties, frustrations, "
                    "or aspirations are involved? Emotional needs often drive purchase decisions "
                    "more than functional needs."
                ),
                temperature=0.7,
                max_tokens=1536,
            ),
            StepDefinition(
                index=3,
                name="Identify Social Needs",
                description="Explore the social dimensions and how others perceive the customer's actions",
                system_prompt=(
                    "You are an expert in Jobs-to-be-Done (JTBD) theory. "
                    "You are continuing a JTBD analysis. "
                    "Identify the social needs — how the customer wants to be perceived "
                    "by others when hiring a solution. What social status, identity, "
                    "or belonging needs are at play? How does the social context "
                    "influence the job?"
                ),
                temperature=0.7,
                max_tokens=1536,
            ),
            StepDefinition(
                index=4,
                name="Synthesize Value Proposition",
                description="Combine all dimensions into a compelling value proposition",
                system_prompt=(
                    "You are an expert in Jobs-to-be-Done (JTBD) theory. "
                    "You are completing a JTBD analysis. "
                    "Synthesize all findings into a clear value proposition that addresses: "
                    "1) The core functional job and outcomes "
                    "2) The emotional needs and feelings "
                    "3) The social needs and perceptions "
                    "4) How a solution can be designed to fulfill all three dimensions "
                    "Provide actionable recommendations for product or service design."
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
                "Please define the core 'job to be done' in this context. "
                "What progress is the customer trying to make? "
                "What is the specific situation or circumstance? "
                "Use the format: 'When [situation], I want to [motivation] "
                "so I can [desired outcome].'"
            )
        elif step_index == 1:
            user_prompt = (
                f"Original context: {question}\n\n"
                f"Job definition (from Step 1):\n{previous_outputs[0]}\n\n"
                "What are the functional needs for this job? "
                "List specific, measurable outcomes the customer wants to achieve. "
                "Focus on practical, objective requirements."
            )
        elif step_index == 2:
            context = "\n\n".join([
                f"Step {i+1}: {out}"
                for i, out in enumerate(previous_outputs)
            ])
            user_prompt = (
                f"Original context: {question}\n\n"
                f"Previous analysis:\n{context}\n\n"
                "What are the emotional needs? How does the customer want to feel? "
                "What anxieties, frustrations, or aspirations are driving their decisions? "
                "Consider both positive emotions (desired) and negative emotions (to avoid)."
            )
        elif step_index == 3:
            context = "\n\n".join([
                f"Step {i+1}: {out}"
                for i, out in enumerate(previous_outputs)
            ])
            user_prompt = (
                f"Original context: {question}\n\n"
                f"Previous analysis:\n{context}\n\n"
                "What are the social needs? How does the customer want to be perceived? "
                "What social status, identity, or belonging factors influence this job? "
                "Consider peer influence, social norms, and public perception."
            )
        elif step_index == 4:
            context = "\n\n".join([
                f"Step {i+1}: {out}"
                for i, out in enumerate(previous_outputs)
            ])
            user_prompt = (
                f"Original context: {question}\n\n"
                f"Full analysis so far:\n{context}\n\n"
                "Based on all the above, synthesize a complete value proposition. "
                "How can a product or service be designed to fulfill the functional, "
                "emotional, and social dimensions of this job? "
                "Provide specific, actionable recommendations."
            )
        else:
            raise ValueError(f"Invalid step index: {step_index}")

        return step.system_prompt, user_prompt
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from utils.gigachat_settings import LLM, ROLE_OF_MESSAGE

class EscalationCheck(BaseModel):
    """Escalation check"""
    needs_escalation: bool = Field(
        description="""Whether the notice requires escalation
        according to specified criteria"""
    )

escalation_prompt = ChatPromptTemplate.from_messages(
    [
        (
            ROLE_OF_MESSAGE,
            """
            Determine whether the following notice received
            from a regulatory body requires immediate escalation.
            Immediate escalation is required when {escalation_criteria}.

            Here's the notice message:

            {message}
            """,
        )
    ]
)

escalation_check_model = LLM

ESCALATION_CHECK_CHAIN = (
    escalation_prompt
    | escalation_check_model.with_structured_output(EscalationCheck)
)
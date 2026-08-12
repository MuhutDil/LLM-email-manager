from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from utils.gigachat_settings import LLM, ROLE_OF_MESSAGE

class BinaryAnswer(BaseModel):
    """Binary answer"""
    is_true: bool = Field(
        description="""Whether the answer to the question is yes or no.
        True if yes otherwise False."""
    )

binary_question_prompt = ChatPromptTemplate.from_messages(
    [
        (
            ROLE_OF_MESSAGE,
            """
            Answer this question as True for "yes" and False for "no".
            No other answers are allowed:

            {question}
            """,
        )
    ]
)

binary_question_model = LLM

BINARY_QUESTION_CHAIN = (
    binary_question_prompt
    | binary_question_model.with_structured_output(BinaryAnswer)
)

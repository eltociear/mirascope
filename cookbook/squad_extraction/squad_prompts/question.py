"""A prompt for asking a question about a paragraph of text.

{
  "exact": 85.34482758620689,
  "f1": 91.55579573683022,
  "total": 116,
  "HasAns_exact": 85.34482758620689,
  "HasAns_f1": 91.55579573683022,
  "HasAns_total": 116
}
"""

from pydantic import BaseModel, Field

from mirascope import BasePrompt, OpenAICallParams, tags


class ExtractedAnswer(BaseModel):
    """The answer to a question about a paragraph of text."""

    answer: str = Field(
        ...,
        description=(
            "The extracted answer to the question. This answer is as concise as "
            "possible, most often just a single word. It is also an exact text match "
            "with text in the provided context."
        ),
    )


@tags(["version:0002"])
class QuestionPrompt(BasePrompt):
    """
    SYSTEM:
    You will be asked a question after you read a paragraph. Your task is to
    answer the question based on the information in the paragraph. Your answer
    should be an exact text match to text from the paragraph. Your answer should
    also be one or two words at most is possible.

    USER:
    {paragraph}

    USER:
    {question}
    """

    paragraph: str
    question: str

    call_params = OpenAICallParams(model="gpt-3.5-turbo-1106")
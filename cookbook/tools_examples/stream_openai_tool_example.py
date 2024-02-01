"""An example demonstrating how to stream `OpenAITool`s tools."""
import os
from typing import Callable, Literal, Type, Union

from pydantic import Field

from mirascope import (
    OpenAIChat,
    OpenAITool,
    PartialOpenAIToolParser,
    Prompt,
    openai_tool_fn,
)

os.environ["OPENAI_API_KEY"] = "YOUR_API_KEY"


class CurrentWeatherPrompt(Prompt):
    """What's the weather like in San Francisco, Tokyo, and Paris?"""


def get_current_weather(
    location: str, unit: Literal["celsius", "fahrenheit"] = "fahrenheit"
) -> str:
    """Returns the current weather in a given location."""
    return f"{location} is 65 degrees {unit}."


@openai_tool_fn(get_current_weather)
class GetCurrentWeather(OpenAITool):
    """Get the current weather in a given location."""

    location: str = Field(..., description="The city and state, e.g. San Francisco, CA")
    unit: Literal["celsius", "fahrenheit"] = "fahrenheit"


chat = OpenAIChat(model="gpt-3.5-turbo-1106")


tools: list[Union[Callable, Type[OpenAITool]]] = [GetCurrentWeather]
stream_completion = chat.stream(
    CurrentWeatherPrompt(),
    tools=tools,  # pass in the function itself for automatic conversion
)
parser = PartialOpenAIToolParser(tools=tools)
for partial_tool in parser.from_stream(stream_completion):
    print("data: ", partial_tool.__dict__, "\n\n")

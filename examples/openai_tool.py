"""An example demonstrating how to use `OpenAITool`s as tools."""
import os
from typing import Literal

from pydantic import Field

from mirascope import BasePrompt, OpenAICallParams, OpenAIChat, OpenAITool, tool_fn

os.environ["OPENAI_API_KEY"] = "YOUR_API_KEY"


def get_current_weather(
    location: str, unit: Literal["celsius", "fahrenheit"] = "fahrenheit"
) -> str:
    """Returns the current weather in a given location."""
    return f"{location} is 65 degrees {unit}."


@tool_fn(get_current_weather)
class GetCurrentWeather(OpenAITool):
    """Get the current weather in a given location."""

    location: str = Field(..., description="The city and state, e.g. San Francisco, CA")
    unit: Literal["celsius", "fahrenheit"] = "fahrenheit"


class CurrentWeatherPrompt(BasePrompt):
    """What's the weather like in San Francisco, Tokyo, and Paris?"""

    call_params = OpenAICallParams(
        model="gpt-3.5-turbo-1106", tools=[GetCurrentWeather]
    )


chat = OpenAIChat()
completion = chat.create(CurrentWeatherPrompt())

if tools := completion.tools:
    for tool in tools:
        print(tool.fn(**tool.args))
"""OpenAI-powered weather agent."""

from __future__ import annotations

import json
from typing import Any

from openai import OpenAI

from .weather_api import OpenMeteoClient, WeatherLookupError


SYSTEM_PROMPT = (
    "You are weather-agent. Your job is to provide a concise but useful weather summary. "
    "When a user asks about a city, call the weather_lookup tool first, then summarize "
    "the current weather and provide a 10-day forecast overview in a readable table/bullets."
)


class WeatherAgent:
    """Coordinates OpenAI tool-calling and the Open-Meteo API."""

    def __init__(self, model: str = "gpt-4o-mini") -> None:
        self._client = OpenAI()
        self._weather = OpenMeteoClient()
        self._model = model

    def close(self) -> None:
        self._weather.close()

    def _run_weather_lookup(self, city: str) -> str:
        try:
            payload = self._weather.get_weather(city)
            return json.dumps(payload)
        except WeatherLookupError as exc:
            return json.dumps({"error": str(exc)})

    def ask(self, city: str) -> str:
        """Ask the agent for weather in a city and return a natural-language answer."""
        tool_schema: list[dict[str, Any]] = [
            {
                "type": "function",
                "name": "weather_lookup",
                "description": "Get current weather and 10-day forecast for a city name.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city": {
                            "type": "string",
                            "description": "The city provided by the user.",
                        }
                    },
                    "required": ["city"],
                    "additionalProperties": False,
                },
            }
        ]

        response = self._client.responses.create(
            model=self._model,
            input=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Get weather for {city}."},
            ],
            tools=tool_schema,
        )

        tool_calls = [item for item in response.output if item.type == "function_call"]

        if not tool_calls:
            return response.output_text

        follow_up_input: list[dict[str, Any]] = []
        for call in tool_calls:
            args = json.loads(call.arguments)
            tool_output = self._run_weather_lookup(args["city"])
            follow_up_input.append(
                {
                    "type": "function_call_output",
                    "call_id": call.call_id,
                    "output": tool_output,
                }
            )

        final = self._client.responses.create(
            model=self._model,
            previous_response_id=response.id,
            input=follow_up_input,
        )
        return final.output_text

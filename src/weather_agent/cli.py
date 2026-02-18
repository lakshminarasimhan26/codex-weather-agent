"""CLI entry point for weather-agent."""

from __future__ import annotations

import argparse

from .agent import WeatherAgent


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="weather-agent",
        description="AI weather agent using OpenAI + Open-Meteo.",
    )
    parser.add_argument("city", help="City name (example: London)")
    parser.add_argument(
        "--model",
        default="gpt-4o-mini",
        help="OpenAI model to use (default: gpt-4o-mini).",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    agent = WeatherAgent(model=args.model)
    try:
        answer = agent.ask(args.city)
        print(answer)
    finally:
        agent.close()


if __name__ == "__main__":
    main()

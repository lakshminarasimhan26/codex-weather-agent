# weather-agent

A simple Python AI agent that uses **OpenAI** for reasoning/response generation and **Open-Meteo** (open-source weather API) for data retrieval.

The agent accepts a city name, fetches:
- current weather
- next 10 days forecast

…and then asks OpenAI to return a clean, human-friendly summary.

---

## 1) Prerequisites

- Python **3.11+**
- [uv](https://docs.astral.sh/uv/) installed
- OpenAI API key

You can install `uv` (one option):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

---

## 2) Project setup (with uv)

From the project root:

```bash
uv sync
```

This creates a virtual environment and installs dependencies from `pyproject.toml`.

Set your OpenAI key:

```bash
export OPENAI_API_KEY="your_api_key_here"
```

> Tip: add this export to your shell profile (`~/.bashrc` or `~/.zshrc`) for convenience.

---

## 3) Run the agent

### Basic usage

```bash
uv run weather-agent "London"
```

### Specify a model

```bash
uv run weather-agent "Tokyo" --model gpt-4o-mini
```

---

## 4) How it works

1. CLI accepts a city name.
2. The app sends a request to OpenAI with a tool schema called `weather_lookup`.
3. OpenAI triggers the tool call.
4. Local Python code calls Open-Meteo geocoding + forecast endpoints.
5. Tool output is sent back to OpenAI.
6. OpenAI returns a final answer containing:
   - current weather summary
   - 10-day forecast overview

---

## 5) Example interactions

### Example A

```bash
uv run weather-agent "New York"
```

Example style of response:

```text
Current weather in New York, US:
- Temperature: 8.4°C (feels like 6.9°C)
- Wind: 12.3 km/h

10-day outlook:
- Day 1: 10° / 4°, rain chance 35%
- Day 2: 9° / 3°, rain chance 20%
...
- Day 10: 7° / 1°, rain chance 10%
```

### Example B

```bash
uv run weather-agent "Bengaluru"
```

Possible response behavior:
- If city is found, the model summarizes current conditions and daily highs/lows.
- If city is not found, it returns a helpful error message.

---

## 6) Development commands

Run tests:

```bash
uv run pytest
```

Run linter:

```bash
uv run ruff check .
```

---

## 7) Key files

- `src/weather_agent/cli.py` — command line entrypoint
- `src/weather_agent/agent.py` — OpenAI tool-calling orchestration
- `src/weather_agent/weather_api.py` — Open-Meteo integration
- `tests/test_cli.py` — basic parser test

---

## 8) Notes and limitations

- Open-Meteo data quality depends on city geocoding and source models.
- Requires internet access for both OpenAI and Open-Meteo.
- The exact response format depends on selected OpenAI model.


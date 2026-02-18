"""Utility functions for looking up weather data from Open-Meteo APIs."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import httpx

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


class WeatherLookupError(RuntimeError):
    """Raised when city lookup or forecast retrieval fails."""


@dataclass
class Coordinates:
    latitude: float
    longitude: float
    name: str
    country: str


class OpenMeteoClient:
    """Client for Open-Meteo geocoding and forecast endpoints."""

    def __init__(self, timeout_s: float = 20.0) -> None:
        self._http = httpx.Client(timeout=timeout_s)

    def close(self) -> None:
        self._http.close()

    def geocode_city(self, city: str) -> Coordinates:
        resp = self._http.get(GEOCODING_URL, params={"name": city, "count": 1, "language": "en", "format": "json"})
        resp.raise_for_status()

        payload = resp.json()
        results = payload.get("results") or []
        if not results:
            raise WeatherLookupError(f"No city found for '{city}'.")

        top = results[0]
        return Coordinates(
            latitude=top["latitude"],
            longitude=top["longitude"],
            name=top["name"],
            country=top.get("country", "Unknown"),
        )

    def get_weather(self, city: str) -> dict[str, Any]:
        location = self.geocode_city(city)

        params = {
            "latitude": location.latitude,
            "longitude": location.longitude,
            "current": ["temperature_2m", "apparent_temperature", "weather_code", "wind_speed_10m"],
            "daily": [
                "weather_code",
                "temperature_2m_max",
                "temperature_2m_min",
                "precipitation_probability_max",
            ],
            "forecast_days": 10,
            "timezone": "auto",
        }

        resp = self._http.get(FORECAST_URL, params=params)
        resp.raise_for_status()
        data = resp.json()

        return {
            "location": {
                "city": location.name,
                "country": location.country,
                "latitude": location.latitude,
                "longitude": location.longitude,
                "timezone": data.get("timezone"),
            },
            "current": data.get("current", {}),
            "daily": data.get("daily", {}),
        }

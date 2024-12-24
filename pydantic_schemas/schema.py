from pydantic import BaseModel
from typing import List

class WeahterResponse(BaseModel):
    temperature: float
    humidity: int
    description: str

class ForecastResponse(BaseModel):
    day: str
    temperature: float
    description: str

class WeatherRequest(BaseModel):
    location: str
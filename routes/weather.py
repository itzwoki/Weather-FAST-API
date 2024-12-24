from fastapi import APIRouter, HTTPException

from pydantic_schemas.schema import WeahterResponse, WeatherRequest, ForecastResponse
from publicapi.weather import fetch_current_weather, fetch_7_day_forecast


router = APIRouter(prefix="/weather")

@router.post("/current", response_model=WeahterResponse)
async def get_current_weather(request: WeatherRequest):
    try:
        weather_data = await fetch_current_weather(request.location)
        return weather_data
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.post("/forecast", response_model=list[ForecastResponse])
async def get_sevenday_forecast(reqest: WeatherRequest):
    try:
        forecast_data = await fetch_7_day_forecast(reqest.location)
        return forecast_data
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

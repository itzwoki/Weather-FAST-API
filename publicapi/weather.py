import httpx

from typing import List

from pydantic_schemas.schema import WeahterResponse, ForecastResponse

OPENWEATHERMAP_API_KEY = "" // get api key from -> https://openweathermap.org/api // Public API key will only provide current weather // for 7-day-forecast 
you will need a paid API key.
BASE_URL = "http://api.openweathermap.org/data/2.5" 


async def get_lat_lon(location: str) -> tuple:
    geocode_url = f"{BASE_URL}/weather?q={location}&appid={OPENWEATHERMAP_API_KEY}"
    async with httpx.AsyncClient() as client:
        response = await client.get(geocode_url)
    data = response.json()
    
    if response.status_code != 200 or 'coord' not in data:
        raise ValueError("Location not found")
    
    return data["coord"]["lat"], data["coord"]["lon"]

async def fetch_current_weather(location: str) -> WeahterResponse:
    url = f"{BASE_URL}/weather?q={location}&appid={OPENWEATHERMAP_API_KEY}&units=metric"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()

        data = response.json()

        if "main" in data and "weather" in data and isinstance(data["weather"], list):
            return WeahterResponse(
                temperature=data["main"]["temp"],
                humidity=data["main"]["humidity"],
                description=data["weather"][0]["description"]
            )
        else:
            raise ValueError("Invalid Data Format Received.")
        
    except httpx.RequestError as exc:
        print(f"An error occurred while requesting data: {exc}")

    except httpx.HTTPStatusError as exc:
        print(f"HTTP error occurred: {exc.response.status_code} - {exc.response.text}")

    except ValueError as exc:

        print(f"Data format error: {exc}")

    return None

async def fetch_7_day_forecast(location: str) -> List[ForecastResponse]:
    latitude, longitude = await get_lat_lon(location)

    url = f"{BASE_URL}/onecall?lat={latitude}&lon={longitude}&exclude=current,minutely,hourly,alerts&appid={OPENWEATHERMAP_API_KEY}&units=metric"
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()

        data = response.json()

        if "daily" not in data:
            raise ValueError ("Invalid data format received: 'daily' not found.")
        
        forecast = [
            ForecastResponse(
                day=str(i),
                temperature=day_data["temp"]["day"],
                description=day_data["weather"][0]["description"]
            )
            for i, day_data in enumerate(data["daily"])
            if "temp" in day_data and "weather" in day_data and isinstance(day_data["weather"], list)
        ]

        return forecast
    
    except httpx.RequestError as exc:
        print(f"An error occurred while requesting data: {exc}")

    except httpx.HTTPStatusError as exc:
        print(f"HTTP error occurred: {exc.response.status_code} - {exc.response.text}")

    except ValueError as exc:
        print(f"Data format error: {exc}")

    return []

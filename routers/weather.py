from fastapi import APIRouter, Depends, HTTPException
from dependencies.dependencies import get_db, get_api_key
import asyncpg
import os
import requests
router = APIRouter()
from utils import utils
import json
@router.post("/weather_query/")
async def weather_query(
    id_user: int,
    city: str,
    api_key: str = Depends(get_api_key),
    conn: asyncpg.Connection = Depends(get_db)
):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={os.getenv('WEATHER_API_KEY')}&units=metric"
        response = requests.get(url)
        if response.status_code == 200:
            weather_data = response.json()

            # Сохранение запроса в базу данных
            return {"weather":[weather_data["name"],
                weather_data["weather"][0]['main'],
                weather_data["weather"][0]["description"],
                weather_data["main"]["temp"],
                weather_data["main"]["feels_like"],
                weather_data["main"]["humidity"],
                utils.hpa_to_mmhg(weather_data["main"]["pressure"]),
                weather_data["wind"]["speed"],
                utils.wind_direction(weather_data["wind"]["deg"]),
                utils.timestamp_to_hms_format(weather_data["sys"]["sunrise"], weather_data["timezone"]),
                utils.timestamp_to_hms_format(weather_data["sys"]["sunset"], weather_data["timezone"]),
                utils.timestamp_to_hms_format(weather_data["dt"], weather_data["timezone"]),
                json.dumps(weather_data)]}


        else:
            raise HTTPException(status_code=500, detail=f"Weather not found")
    except asyncpg.PostgresError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

@router.get("/get_weather_history/{id_user}")
async def get_weather_history(id_user: int, api_key: str = Depends(get_api_key), conn: asyncpg.Connection = Depends(get_db)):
    try:
        history = await conn.fetch(
            """
            SELECT query_timestamp, city_name, weather_main, weather_description, temperature, temperature_feels_like, 
            humidity, pressure, wind_speed, wind_direction, sunrise, sunset, data_calculation 
            FROM weather_queries WHERE id_user=$1 
            ORDER BY query_timestamp DESC
            """,
            id_user
        )
        return history
    except asyncpg.PostgresError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
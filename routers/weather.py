from fastapi import APIRouter, Depends, HTTPException
from dependencies.dependencies import get_db, get_api_key
import asyncpg
import os
import requests
router = APIRouter()
from utils import utils
import json
@router.get("/weather_query/")
async def weather_query(
    id_user: int,
    city: str,
    api_key: str = Depends(get_api_key),
    conn: asyncpg.Connection = Depends(get_db)
):
    print(id_user,city)
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={os.getenv('WEATHER_API_KEY')}&units=metric"
        response = requests.get(url)
        if response.status_code == 200:
            weather_data = response.json()
            print(weather_data)
            # Сохранение запроса в базу данных
            return weather_data


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
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from dependencies.dependencies import get_db, get_api_key
import asyncpg
import os
import requests
router = APIRouter()
from utils import utils
import json
from datetime import datetime

@router.get("/get_notification_time/")
async def get_notification_time_by_id_user(id_user: int,notification_type:str,api_key: str = Depends(get_api_key),conn: asyncpg.Connection = Depends(get_db)):
    try:
        res=await conn.fetch("SELECT notification_time FROM notification_times WHERE id_user=$1 AND notification_type=$2",id_user,notification_type)
        if res:
            return JSONResponse(
                status_code=200,
                content=dict(res)
            )
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except asyncpg.PostgresError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

@router.post("/set_notification_time/")
async def set_notification_time(id_user: int,notification_type:str,notification_time:str,api_key: str = Depends(get_api_key),conn: asyncpg.Connection = Depends(get_db)):
    try:
        # Преобразуем строку времени в объект времени
        time_obj = datetime.strptime(notification_time, '%H:%M').time()

        # Вставляем новую запись в таблицу
        await conn.execute(
            "INSERT INTO notification_times (id_user, notification_time, notification_type) VALUES ($1, $2, $3)",
            id_user, time_obj, notification_type
        )

        return JSONResponse(
            status_code=200,
            content={"message": "Notification time added successfully"}
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid time format: {e}")
    except asyncpg.PostgresError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")


@router.delete("/delete_notification_time/")
async def delete_notification_time(
        id_user: int,
        notification_time: str,  # Время в формате 'hh:mm'
        api_key: str = Depends(get_api_key),
        conn: asyncpg.Connection = Depends(get_db)
):
    try:
        # Преобразуем строку времени в объект времени
        time_obj = datetime.strptime(notification_time, '%H:%M').time()

        # Удаляем запись из таблицы
        result = await conn.execute(
            "DELETE FROM notification_times WHERE id_user = $1 AND notification_time = $2",
            id_user, time_obj
        )

        # Проверяем, была ли удалена хотя бы одна запись
        if result == "DELETE 0":
            raise HTTPException(status_code=404, detail="Notification time not found for the given user and time")

        return JSONResponse(
            status_code=200,
            content={"message": "Notification time deleted successfully"}
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid time format: {e}")
    except asyncpg.PostgresError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
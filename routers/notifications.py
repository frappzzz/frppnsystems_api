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


@router.get("/get_notifications_by_time/")
async def get_notifications_by_time(
        notification_time: str,  # Время в формате 'hh:mm'
        api_key: str = Depends(get_api_key),
        conn: asyncpg.Connection = Depends(get_db)
):
    try:
        # Преобразуем строку времени в объект времени
        time_obj = datetime.strptime(notification_time, '%H:%M').time()

        # Получаем список пользователей, у которых есть уведомления на это время
        notifications = await conn.fetch(
            """
            SELECT u.id_user_tg, u.home_city 
            FROM notification_times nt
            JOIN users u ON nt.id_user = u.id_user
            WHERE nt.notification_time = $1 AND nt.notification_type = 'weather'
            """,
            time_obj
        )

        # Преобразуем записи в список словарей
        notifications_list = [dict(record) for record in notifications]

        return JSONResponse(
            status_code=200,
            content=notifications_list
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid time format: {e}")
    except asyncpg.PostgresError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
@router.post("/set_notification_time/")
async def set_notification_time(
    id_user: int,
    notification_type: str,
    notification_time: str,  # Время в формате 'hh:mm'
    api_key: str = Depends(get_api_key),
    conn: asyncpg.Connection = Depends(get_db)
):
    try:
        # Преобразуем строку времени в объект времени
        time_obj = datetime.strptime(notification_time, '%H:%M').time()

        # Проверяем, существует ли уже такая запись
        existing_record = await conn.fetchrow(
            "SELECT * FROM notification_times WHERE id_user = $1 AND notification_time = $2 AND notification_type = $3",
            id_user, time_obj, notification_type
        )

        if existing_record:
            raise HTTPException(
                status_code=400,
                detail="Notification time already exists for this user and type"
            )

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
@router.get("/get_notifications_by_id_user")
async def get_notifications_by_id_user(id_user: str,  # Время в формате 'hh:mm'
        api_key: str = Depends(get_api_key),
        conn: asyncpg.Connection = Depends(get_db)
):
    try:

        # Проверяем, существует ли уже такая запись
        existing_result = await conn.fetch(
            "SELECT * FROM notification_times WHERE id_user = $1",
            id_user
        )
        return existing_result
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
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

@router.get("/check_id_user_tg/{id_user_tg}")
async def check_id_user_tg(id_user_tg: int,api_key: str = Depends(get_api_key),conn: asyncpg.Connection = Depends(get_db)):
    print(id_user_tg)
    try:
        res=await conn.fetchrow("SELECT id_user_tg FROM users WHERE id_user_tg=$1",id_user_tg)
        if res:
            return JSONResponse(
                status_code=200,
                content=dict(res)
            )
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except asyncpg.PostgresError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
@router.get("/get_id_user_by_id_user_tg/{id_user_tg}")
async def get_id_user_by_id_user_tg(id_user_tg: int,api_key: str = Depends(get_api_key),conn: asyncpg.Connection = Depends(get_db)):
    try:
        res=await conn.fetchrow("SELECT id_user FROM users WHERE id_user_tg=$1",id_user_tg)
        if res:
            return JSONResponse(
                status_code=200,
                content=dict(res)
            )
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except asyncpg.PostgresError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

@router.post("/set_user_name/")
async def set_user_name(id_user: int,user_name:str,api_key: str = Depends(get_api_key),conn: asyncpg.Connection = Depends(get_db)):
    try:
        await conn.execute("UPDATE users SET name=$1 WHERE id_user=$2", user_name, id_user)
        return JSONResponse(
            status_code=200,
            content={"message": "Name updated successfully"}
        )
    except asyncpg.PostgresError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
@router.post("/set_user_home_city/")
async def set_user_home_city(id_user: int,home_city:str,api_key: str = Depends(get_api_key),conn: asyncpg.Connection = Depends(get_db)):
    try:
        await conn.execute("UPDATE users SET home_city=$1 WHERE id_user=$2", home_city, id_user)
        return JSONResponse(
            status_code=200,
            content={"message": "Home city updated successfully"}
        )
    except asyncpg.PostgresError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
@router.get("/get_user_by_id_user/{id_user}")
async def get_user_by_id_user(id_user: int,api_key: str = Depends(get_api_key),conn: asyncpg.Connection = Depends(get_db)):
    try:
        res=await conn.fetchrow("SELECT * FROM users WHERE id_user=$1",id_user)
        if res:
            return JSONResponse(
                status_code=200,
                content=dict(res)
            )
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except asyncpg.PostgresError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
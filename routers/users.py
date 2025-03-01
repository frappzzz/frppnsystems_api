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
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



@router.get("/generate_auth_key")
async def generate_auth_key(api_key: str = Depends(get_api_key),conn: asyncpg.Connection = Depends(get_db)):
    auth_key=utils.generate_code()
    try:
        await conn.execute("INSERT INTO auth_keys (id_user_tg, auth_key) VALUES (0,$1)",auth_key)
        return auth_key
    except asyncpg.PostgresError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
@router.get("/check_auth_key/{auth_key}")
async def check_auth_key(auth_key: str,api_key: str = Depends(get_api_key),conn: asyncpg.Connection = Depends(get_db)):
    print(auth_key)
    try:
        res=await conn.fetchrow("SELECT auth_key FROM auth_keys WHERE auth_key=$1",auth_key)
        if res:
            return JSONResponse(
                status_code=200,
                content=dict(res)
            )
        else:
            raise HTTPException(status_code=404, detail="Key not found")
    except asyncpg.PostgresError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

@router.post("/auth_user/")
async def auth_user(auth_key: str,id_user_tg: int,api_key: str = Depends(get_api_key),conn: asyncpg.Connection = Depends(get_db)):
    print(auth_key)
    print(id_user_tg)
    try:
        res = await conn.fetchrow("SELECT auth_key FROM auth_keys WHERE auth_key=$1", auth_key)
        if not res:
            raise HTTPException(status_code=404, detail="Key not found")
        await conn.execute("UPDATE auth_keys SET id_user_tg=$1 WHERE auth_key=$2", id_user_tg,auth_key)
        await conn.execute("INSERT INTO users (id_user_tg, name, home_city) VALUES ($1,$2,$3)",id_user_tg,"anonymous","unknown")
        return JSONResponse(
            status_code=200,
            content={"message": "User authorized successfully"}
        )
    except asyncpg.PostgresError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
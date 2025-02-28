from fastapi.security import APIKeyHeader
from fastapi import HTTPException, status, Depends
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY_NAME = os.getenv("FASTAPI_KEY_NAME")
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

def get_api_key(api_key: str = Depends(api_key_header)):
    if api_key == os.getenv("FASTAPI_TOKEN"):
        return api_key
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or missing API Key",
        )

async def create_db_pool():
    return await asyncpg.create_pool(os.getenv("DB_URL"), max_inactive_connection_lifetime=3)

async def get_db():
    pool = await create_db_pool()
    async with pool.acquire() as connection:
        yield connection
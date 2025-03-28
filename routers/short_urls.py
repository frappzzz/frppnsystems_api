from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse, RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime, timedelta
from models.models import ShortUrlCreate, ShortUrlResponse
from utils.utils import generate_short_code
from dependencies.dependencies import get_db
import asyncpg

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/shortener", response_class=HTMLResponse)
async def shortener_page(request: Request):
    """Отображает HTML страницу для сокращения ссылок"""
    return templates.TemplateResponse("shortener.html", {"request": request})

async def generate_unique_short_code(conn: asyncpg.Connection):
    """Генерирует уникальный код с проверкой в БД"""
    attempts = 0
    max_attempts = 10

    while attempts < max_attempts:
        code = generate_short_code()
        exists = await conn.fetchval(
            "SELECT 1 FROM short_urls WHERE short_code = $1", code
        )
        if not exists:
            return code
        attempts += 1

    raise HTTPException(
        status_code=500,
        detail="Не удалось сгенерировать уникальный код"
    )

@router.post("/shorten/", response_model=ShortUrlResponse)
async def create_short_url(
    url_data: ShortUrlCreate,
    conn: asyncpg.Connection = Depends(get_db)
):
    """Создает новую короткую ссылку"""
    short_code = url_data.custom_code or await generate_unique_short_code(conn)

    expires_at = None
    if url_data.expires_days:
        expires_at = datetime.now() + timedelta(days=url_data.expires_days)

    try:
        if url_data.custom_code:
            exists = await conn.fetchval(
                "SELECT 1 FROM short_urls WHERE short_code = $1",
                short_code
            )
            if exists:
                raise HTTPException(
                    status_code=400,
                    detail="Указанный код уже используется"
                )

        record = await conn.fetchrow(
            """
            INSERT INTO short_urls 
            (original_url, short_code, expires_at) 
            VALUES ($1, $2, $3)
            RETURNING id, original_url, short_code, created_at, expires_at, clicks
            """,
            url_data.original_url, short_code, expires_at
        )

        return {
            **dict(record),
            "short_url": f"http://185.43.4.64:5000/{short_code}"  # Замените на ваш домен
        }

    except asyncpg.PostgresError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка базы данных: {e}"
        )

@router.get("/{short_code}")
async def redirect_short_url(
    short_code: str,
    conn: asyncpg.Connection = Depends(get_db)
):
    """Перенаправляет по короткой ссылке"""
    record = await conn.fetchrow(
        """
        SELECT original_url, clicks 
        FROM short_urls 
        WHERE short_code = $1 AND is_active = TRUE 
          AND (expires_at IS NULL OR expires_at > NOW())
        """,
        short_code
    )

    if not record:
        raise HTTPException(
            status_code=404,
            detail="Ссылка не найдена или срок ее действия истек"
        )

    await conn.execute(
        "UPDATE short_urls SET clicks = $1 WHERE short_code = $2",
        record['clicks'] + 1, short_code
    )

    return RedirectResponse(record['original_url'])

@router.get("/stats/{short_code}", response_model=ShortUrlResponse)
async def get_short_url_stats(
    short_code: str,
    conn: asyncpg.Connection = Depends(get_db)
):
    """Получает статистику по короткой ссылке"""
    record = await conn.fetchrow(
        """
        SELECT id, original_url, short_code, created_at, expires_at, clicks
        FROM short_urls 
        WHERE short_code = $1
        """,
        short_code
    )

    if not record:
        raise HTTPException(
            status_code=404,
            detail="Ссылка не найдена"
        )

    return {
        **dict(record),
        "short_url": f"http://185.43.4.64:5000/{short_code}"
    }
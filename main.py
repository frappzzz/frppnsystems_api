from fastapi import FastAPI
from dotenv import load_dotenv
import os

# Загружаем переменные окружения из .env файла
load_dotenv()

app = FastAPI()

# Подключаем роутеры
from routers import weather

app.include_router(weather.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
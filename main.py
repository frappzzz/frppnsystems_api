from fastapi import FastAPI
from dotenv import load_dotenv
import os

# Загружаем переменные окружения из .env файла
load_dotenv()

app = FastAPI()

# Подключаем роутеры
from routers import weather, auth, users

app.include_router(weather.router)
app.include_router(auth.router)
app.include_router(users.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
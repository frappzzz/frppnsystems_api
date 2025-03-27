from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

# Подключаем статические файлы (CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Подключаем роутеры
from routers import weather, auth, users, notifications, short_urls

app.include_router(weather.router)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(notifications.router)
app.include_router(short_urls.router, tags=["URL Shortener"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
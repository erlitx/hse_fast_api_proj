import string
import random
import os

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from sqlalchemy.orm import Session
from adapter.sqllite_apapter import URL, get_db


# Создаем приложение FastAPI
app = FastAPI()

HOST = os.getenv("HOST", "localhost")
PORT = os.getenv("PORT", "8001")


# --- Утилиты ---
# Генерация случайного короткого идентификатора
def generate_short_id(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


# --- Модель Pydantic для запроса ---
class URLRequest(BaseModel):
    url: str


# --- Эндпоинты ---
# 1. Создание короткой ссылки
@app.post("/shorten")
def shorten_url(request: URLRequest, client_request: Request, db: Session = Depends(get_db)):
    full_url = request.url

    if not full_url.startswith("http"):
        raise HTTPException(status_code=400, detail="URL должен начинаться с http или https")

    # Генерация уникального short_id
    short_id = generate_short_id()
    while db.query(URL).filter(URL.short_id == short_id).first():
        short_id = generate_short_id()

    # Сохранение в базе данных
    new_url = URL(short_id=short_id, full_url=full_url)
    db.add(new_url)
    db.commit()
    db.close()

    # Создаем ссылку динамически, берем URL из request
    base_url = str(client_request.base_url).rstrip("/")
    return {"short_id": short_id, "short_url": f"{base_url}/{short_id}"}


# 2. Перенаправление по короткой ссылке
@app.get("/{short_id}")
def redirect_to_url(short_id: str, db: Session = Depends(get_db)):

    url_entry = db.query(URL).filter(URL.short_id == short_id).first()
    db.close()

    if not url_entry:
        raise HTTPException(status_code=404, detail="Короткий идентификатор не найден")

    return RedirectResponse(url=url_entry.full_url)


# 3. Получение инфы по короткой ссылке
@app.get("/stats/{short_id}")
def get_url_stats(short_id: str, db: Session = Depends(get_db)):
    url_entry = db.query(URL).filter(URL.short_id == short_id).first()
    db.close()
    if not url_entry:
        raise HTTPException(status_code=404, detail="Короткий идентификатор не найден")

    return {"short_id": short_id, "full_url": url_entry.full_url}




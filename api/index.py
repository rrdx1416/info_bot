import os
import sys
from aiogram import Bot, Dispatcher
from aiogram.types import Update
from fastapi import FastAPI, HTTPException, Request

from app.handlers import router
from config import settings

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


SECRET = os.getenv("WEBHOOK_SECRET", "")

dp = Dispatcher()
dp.include_router(router)

app = FastAPI()


@app.post("/api/webhook")
async def webhook(request: Request):
    if (
        SECRET
        and request.headers.get("x-telegram-bot-api-secret-token") != SECRET
    ):
        raise HTTPException(status_code=403)

    bot = Bot(settings.bot_token)
    try:
        update = Update.model_validate(
            await request.json(), context={"bot": bot}
        )
        await dp.feed_update(bot, update)
    finally:
        await bot.session.close()
    return {"ok": True}


@app.get("/api/set-webhook")
async def set_webhook(request: Request):
    bot = Bot(settings.bot_token)
    try:
        url = f"https://{request.headers['host']}/api/webhook"
        ok = await bot.set_webhook(url, secret_token=SECRET or None)
    finally:
        await bot.session.close()
    return {"ok": ok, "url": url}

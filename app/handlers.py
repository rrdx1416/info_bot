from datetime import timezone

from aiogram import Bot, Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.utils import build_admin_text, send_greeting
from config import settings

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, bot: Bot) -> None:
    user = message.from_user
    if user is None:
        return

    started_at = message.date.astimezone(timezone.utc)

    await send_greeting(message)

    await bot.send_message(
        settings.admin_id,
        build_admin_text(user, started_at),
    )

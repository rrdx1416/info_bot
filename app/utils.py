from datetime import datetime
from html import escape

from aiogram.types import FSInputFile, Message, User

from config import settings


def build_admin_text(user: User, started_at: datetime) -> str:
    def value(val: object) -> str:
        return escape(str(val)) if val is not None else "Не указано"

    premium = (
        "Да"
        if user.is_premium
        else "Нет" if user.is_premium is False else "Не указано"
    )

    username = f"@{user.username}" if user.username else None

    return (
        "🆕 Пользователь запустил бота!\n\n"
        f"ID:{user.id}\n"
        f"Username: {value(username)}\n"
        f"Имя: {value(user.first_name)}\n"
        f"Фамилия: {value(user.last_name)}\n"
        f"Язык: {value(user.language_code)}\n"
        f"Telegram Premium: {premium}\n"
        f"Дата запуска: {started_at:%d.%m.%Y}\n"
        f"Время запуска (UTC): {started_at:%H:%M:%S}"
    )


async def send_greeting(message: Message) -> None:
    media = FSInputFile(settings.media_path)
    # fmt: off
    PAD = "\u2800" * 17

    welcome_caption = (
        f"{PAD}\n"
        f"{PAD}@nndx16\n"
        f"{PAD}"
    )
    # fmt: on

    if settings.media_path.suffix.lower() == ".gif":
        await message.answer_animation(
            animation=media,
            caption=welcome_caption,
        )
    else:
        await message.answer_photo(
            photo=media,
            caption=welcome_caption,
        )

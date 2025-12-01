import os
import asyncio
import re
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    raise RuntimeError("Не задан TELEGRAM_BOT_TOKEN в переменных окружения")

bot = Bot(token=TOKEN)
dp = Dispatcher()


def normalize_text(text: str) -> str:
    # приведение к нижнему регистру, убираем лишние знаки
    cleaned = re.sub(r"[\n\r]", " ", text).strip().lower()
    # убираем лишние пробелы по краям
    cleaned = cleaned.strip()
    return cleaned


TRIGGERS = {
    "да": "кабзда!",
    "нет": "с-маркетинга ответ!",
    "300": ")))))))))",
    "триста": ")))))))))",
}


@dp.message(CommandStart())
async def cmd_start(message: Message):
    text = (
        "Привет, я чат-бот для групповых чатов.\n\n"
        "В чатах я реагирую ТОЛЬКО на точные фразы:\n"
        "• «да» → «кабзда!»\n"
        "• «нет» → «с-маркетинга ответ!»\n"
        "• «300» или «триста» → «)))))))))»\n\n"
        "Любые другие сообщения я игнорирую."
    )
    await message.answer(text)


@dp.message(Command("help"))
async def cmd_help(message: Message):
    text = (
        "Как я работаю в чатах:\n"
        "• Смотрю только на текстовые сообщения.\n"
        "• Беру текст, привожу к нижнему регистру и обрезаю пробелы.\n"
        "• Реагирую ТОЛЬКО если сообщение целиком одно из:\n"
        "    «да», «нет», «300», «триста».\n\n"
        "Триггеры:\n"
        "• «да» → «кабзда!»\n"
        "• «нет» → «с-маркетинга ответ!»\n"
        "• «300» или «триста» → «)))))))))»"
    )
    await message.answer(text)


@dp.message()
async def react_to_triggers(message: Message):
    # не реагируем на свои сообщения
    me = await bot.me()
    if message.from_user and message.from_user.id == me.id:
        return

    if not message.text:
        return

    norm = normalize_text(message.text)

    reply_text = TRIGGERS.get(norm)
    if reply_text:
        await message.reply(reply_text)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

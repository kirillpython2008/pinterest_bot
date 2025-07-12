from aiogram import Router
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart

from parsing import get_file
from validation import is_link

link_router = Router()


@link_router.message(CommandStart())
async def command_start(message: Message):
    welcome_text = f"""
    ✨ <b>Привет, {message.from_user.first_name}!</b> ✨

    Я — твой личный помощник для скачивания контента с Pinterest! 🎨📥

    <b>Что я умею:</b>
    📌 Скачивать фото и видео по ссылке 🖼️🎬
    📌 Сохранять контент в максимальном качестве 💎

    <b>Как пользоваться:</b>
    1. Просто пришли мне ссылку на пин 🔗
    2. Выбери формат (фото/видео) 📁
    3. Получи готовый файл! ⚡

    🚀 <i>Начни прямо сейчас — отправь мне ссылку!</i>
    """

    await message.answer(welcome_text, parse_mode="HTML")



@link_router.message()
async def download_file(message: Message):
    if await is_link(message.text):
        get_file(message.text)
    else:
        await message.answer_photo(photo=FSInputFile("warning.png"))

from aiogram import Router
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart

from parsing import download_video
from validation import is_link
from db import create_user, check_user_in_db

user_router = Router()


@user_router.message(CommandStart())
async def command_start(message: Message):
    user_id = str(message.from_user.id)
    username = message.from_user.username

    if not(await check_user_in_db(user_id)):
        await create_user(user_id, username)

    welcome_text = f"""
    ✨ <b>Привет, {message.from_user.first_name}!</b> ✨

    Я — твой личный помощник для скачивания контента с Pinterest! 🎨📥

    <b>Что я умею:</b>
    📌 Скачивать видео по ссылке 🖼️🎬
    📌 Сохранять контент в максимальном качестве 💎

    <b>Как пользоваться:</b>
    1. Просто пришли мне ссылку на пин 🔗
    2. Получи готовый файл! ⚡

    🚀 <i>Начни прямо сейчас — отправь мне ссылку!</i>
    """

    await message.answer(welcome_text, parse_mode="HTML")


@user_router.message()
async def download_file(message: Message):
    user_id = message.from_user.id

    if await is_link(message.text):
        if download_video(message.text, str(user_id)):
            await message.answer_video(video=FSInputFile(f"media/media_{user_id}.mp4"))
        else:
            await message.answer("Не удалось скачать видео")
    else:
        await message.answer_photo(photo=FSInputFile("warning.png"))

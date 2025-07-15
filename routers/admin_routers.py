from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.middleware import FSMContext

from db import create_admin, get_admins, get_admin, count_all_users, all_admins, delete_admin, check_admin_in_db
from states.admin_states import AdminStates

admin_router = Router()

get_all_admins = get_admins()

admin_router.message.filter(F.from_user.id.in_(get_all_admins))


@admin_router.message(Command("stat"))
async def statistic(message: Message):
    count_users = await count_all_users(count=1)

    await message.answer(f"Статистика пользователей за все время: {count_users}")


@admin_router.message(Command("all_admins"))
async def get_all_admins(message: Message):
    admins = await all_admins()

    await message.answer("Данные всех админов:")

    for admin in admins:
        await message.answer(str(admin[0]))


@admin_router.message(Command("all_users"))
async def get_all_admins(message: Message):
    users = await count_all_users(count=0)

    await message.answer("Все пользователи:")

    for user in users:
        await message.answer(str(user[0]))


@admin_router.message(Command("delete"))
async def delete_admin_1(message: Message, state: FSMContext):
    await state.set_state(AdminStates.delete_admin)
    await message.answer("Enter a admin id")


@admin_router.message(AdminStates.delete_admin)
async def delete_admin_2(message: Message, state: FSMContext):
    admin_id = message.text
    if await check_admin_in_db(admin_id=admin_id):
        await delete_admin(admin_id=admin_id)

        await message.answer("Админ удален")

    else:
        await message.answer("Админ не найден")

    await state.clear()


@admin_router.message(Command("add_admin"))
async def add_admin_1(message: Message, state: FSMContext):
    await state.set_state(AdminStates.add_admin)
    await message.answer("Enter a admin id")


@admin_router.message(AdminStates.add_admin)
async def add_admin_2(message: Message, state: FSMContext):
    user_id = message.text
    await create_admin(user_id=user_id)
    await state.clear()
    await message.answer("Admin has been created")


@admin_router.message(Command("get_admin"))
async def get_admin_1(message: Message, state: FSMContext):
    await state.set_state(AdminStates.get_admin)
    await message.answer("Enter a admin id")


@admin_router.message(AdminStates.get_admin)
async def get_admin_2(message: Message, state: FSMContext):
    admin_id = message.text
    try:
        admin = await get_admin(user_id=admin_id)

        await message.answer(f"Инфа по админу")
        await message.answer(str(admin))
    except:
        await message.answer("Админ не найден")

    await state.clear()

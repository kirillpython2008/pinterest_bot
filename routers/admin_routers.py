from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.middleware import FSMContext

from db import create_admin, get_admins, get_admin
from states.admin_states import AdminStates

admin_router = Router()

all_admins = get_admins()

admin_router.message.filter(F.from_user.id.in_(all_admins))

@admin_router.message(Command("add_admin"))
async def add_admin_1(message: Message, state: FSMContext):
    await state.set_state(AdminStates.add_admin)
    await message.answer("Enter a admin id")


@admin_router.message(AdminStates.add_admin)
async def add_admin_2(message: Message, state: FSMContext):
    user_id = message.text
    create_admin(user_id=user_id)
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
        admin = get_admin(user_id=admin_id)

        await message.answer(
            f"Инфа по админу\nid: {admin.id}\nuser_id: {admin.user_id}\nusername: {admin.username}")
    except:
        await message.answer("Админ не найден")

    await state.clear()

import random, string, os, django
from aiogram import Bot, Dispatcher, Router, F, types
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
from datetime import datetime

from aiogram.utils.keyboard import InlineKeyboardBuilder
from werkzeug.security import generate_password_hash, check_password_hash
from django.core.cache import cache

''' django setup '''
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()

from services import Register, Login
from telegram_bot.models import User

router = Router()


@router.message(Command("start"))
async def start(clb: CallbackQuery):
    email, password = f"{clb.from_user.id}@telegram.org", str(round(datetime.now().timestamp()))
    user = User.objects.get_or_create(
        email=email,
        defaults={
            "user_id": clb.from_user.id,
            "email": email,
            "password": generate_password_hash(password)
        })[0]

    cache_key = f"telegram_bot_{user.email}"
    authorized = cache.get(key=cache_key)

    if not authorized:
        Register.Register(data={"email": user.email, "password": user.password}, need_execute_local=True)
        login = Login.Login(data={"email": user.email, "password": user.password}, need_execute_local=True).get_response()
        expires_in, token = login["result"]["expires_in"], login["result"]["access_token"]

        cache.set(key=cache_key, value={"email": user.email, "token": token, "expires_in": expires_in}, timeout=expires_in)

    await main_menu(clb)


@router.callback_query(F.data == "main_menu")
async def main_menu(clb: CallbackQuery):
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(text='Модели', callback_data='select_model'))
    builder.row(InlineKeyboardButton(text='Профиль', callback_data='account'))
    builder.row(InlineKeyboardButton(text='Помощь', callback_data='help'))

    await clb.answer(
        text="""
        Добро пожаловать в Bot-X!\n
Я ваш личный телеграмм-помощник, который облегчит вам жизнь, отвечая на вопросы и поддерживая с вами общение.\n
Чтобы начать диалог, выберите одну из моделей ниже и задайте интересующий вас вопрос.
        """,
        reply_markup=builder.as_markup()
    )

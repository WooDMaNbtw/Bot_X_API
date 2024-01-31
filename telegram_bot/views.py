import random, string, os, django
from aiogram import Bot, Dispatcher, Router, F, types
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
from datetime import datetime
import requests
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
    cache_key = f"telegram_bot_{clb.from_user.id}"
    cached_user = cache.get(key=cache_key)

    if not cached_user:
        email, password = f"{clb.from_user.id}@telegram.org", str(round(datetime.now().timestamp()))
        user = User.objects.filter(email=email).first()
        if not user:
            user = User.objects.create(user_id=clb.from_user.id, email=email, password=password)
            register = Register.Register(data={"email": user.email, "password": user.password}, need_execute_local=True)

            if register._status_code == 200:
                await clb.answer("Successful registration")
            elif register._status_code == 404:
                await clb.answer("No data was found, please try again later")
            elif register._status_code == 409:
                await clb.answer("User already exists")
            elif register._status_code == 500:
                await clb.answer("Server error, please try again later")

        login = Login.Login(data={"email": user.email, "password": user.password}, need_execute_local=True)
        login_response = login.get_response()
        if login._status_code == 200:
            expires_in = login_response.get("expires_in", 60)
            token = login_response.get("access_token", None)
            if not token:
                await clb.answer("Token was not provided...")
                raise requests.exceptions.ProxyError("Invalid token")

            cache.set(key=cache_key, value={"email": user.email, "token": token}, timeout=expires_in)
            await main_menu(clb)

        elif login._status_code == 401:
            await clb.answer("Invalid email or password")
        elif login._status_code == 404:
            await clb.answer("No data was found, please try again later")
        elif login._status_code == 500:
            await clb.answer("Server error, please try again later")
    else:
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

import os, django, requests
from typing import Any
from aiogram.filters import Command
from aiogram.types import CallbackQuery
from datetime import datetime
from django.core.cache import cache
from .main_menu import main_menu
from telegram_bot.run import router
from services import Register, Login
from telegram_bot.models import User


async def log_user(clb: CallbackQuery, user: User, login_status_options: dict) -> Any:
    login = Login.Login(data={"email": user.email, "password": user.password}, need_execute_local=True)
    login_response = login.get_response()

    log_status_res = login_status_options[login._status_code]
    if type(log_status_res) is str:
        return await clb.answer(text=log_status_res)
    elif log_status_res is object:
        expires_in = login_response.get("expires_in", 60)
        token = login_response.get("access_token", None)

        if not token:
            await clb.answer("Token was not provided...")
            raise requests.exceptions.ProxyError("Invalid token")

        cache.set(key=f"telegram_bot_{clb.from_user.id}", value={"email": user.email, "token": token},
                  timeout=expires_in)


@router.message(Command("start"))
async def start(clb: CallbackQuery):
    register_status_options = {
        200: Login.Login,
        404: "No data was found, please try again later",
        409: "User already exists",
        500: "Server error, please try again later"
    }

    login_status_options = {
        200: object,
        401: "Invalid email or password",
        404: "No data was found, please try again later",
        500: "Server error, please try again later"
    }

    email, password = f"{clb.from_user.id}@telegram.org", str(round(datetime.now().timestamp()))
    user = User.objects.filter(email=email).first()

    if user:
        cached_user = cache.get(key=f"telegram_bot_{clb.from_user.id}")
        if not cached_user:
            await log_user(clb=clb, user=user, login_status_options=login_status_options)

    elif not user:
        user = User.objects.create(user_id=clb.from_user.id, email=email, password=password)
        register = Register.Register(data={"email": user.email, "password": user.password}, need_execute_local=True)
        register_response = register.get_response()
        reg_status_res = register_status_options[register._status_code]
        if type(reg_status_res) is str:
            return await clb.answer(text=reg_status_res)
        elif reg_status_res is Login.Login:
            user.user_core_id = register_response.get("user_id", None)
            user.save()
            await log_user(clb=clb, user=user, login_status_options=login_status_options)

    return await main_menu(clb)


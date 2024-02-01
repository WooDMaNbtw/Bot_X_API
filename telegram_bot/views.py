import random, string, os, django
from aiogram import Bot, Dispatcher, Router, F, types
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
from datetime import datetime
import requests
from aiogram.utils.keyboard import InlineKeyboardBuilder
from werkzeug.security import generate_password_hash, check_password_hash
from django.core.cache import cache
import requests
from itertools import groupby
from operator import itemgetter
from telegram_bot.assets import HELP_MESSAGE, WELCOME_MESSAGE

''' django setup '''
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()

from services import Register, Login, BotList, BotDetail, DialogueList
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
            return await main_menu(clb)

        elif login._status_code == 401:
            await clb.answer("Invalid email or password")
        elif login._status_code == 404:
            await clb.answer("No data was found, please try again later")
        elif login._status_code == 500:
            await clb.answer("Server error, please try again later")
    else:
        return await main_menu(clb)


@router.callback_query(F.data == "main_menu")
async def main_menu(clb: CallbackQuery):
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(text='Модели', callback_data='select_model'))
    builder.row(InlineKeyboardButton(text='Профиль', callback_data='account'))
    builder.row(InlineKeyboardButton(text='Помощь', callback_data='help'))

    await clb.answer(
        text=WELCOME_MESSAGE,
        reply_markup=builder.as_markup()
    )


def get_bot_list():
    response = BotList.BotList(need_execute_local=True)
    if response._status_code == 200:
        response = response.get_response()
    else:
        return {'error': ['core AFK']}

    bot_list = {}
    for i in response['result']:
        if i['author'] in bot_list:
            bot_list[i['author']].append(i['name'])
        else:
            bot_list[i['author']] = [i['name']]

    return bot_list


def add_buttons(builder, items, key_prefix, back_prefix):
    for i in items:
        builder.add(InlineKeyboardButton(text=i, callback_data=f"{key_prefix}:{i}"))
    builder.row(InlineKeyboardButton(text='<- BACK', callback_data=f'{back_prefix}'))


@router.callback_query(F.data.startswith("select_model"))
async def select_model(callback: CallbackQuery):
    #  bot_list = get_bot_list()

    bot_list_response = BotList.BotList(need_execute_local=True).get_response()
    # Сортируем данные по авторам и именам моделей
    sorted_data = sorted(bot_list_response, key=itemgetter("author", "model_name"))

    # Группируем данные по авторам
    bot_list_result = {key: [item["model_name"] for item in group] for key, group in
                    groupby(sorted_data, key=itemgetter("author"))}

    # bot_list = {'1111': ['aaaa', 'bbbb', 'cccc'], '2222': ['dddd', 'ffff']}
    models = []
    builder = InlineKeyboardBuilder()

    if callback.data == 'select_model':
        if len(bot_list_result) > 1:
            models = list(bot_list_result)
            add_buttons(builder, models, 'select_model', 'main_menu')

        else:
            key, models = bot_list_result.popitem()
            add_buttons(builder, models, 'start_use', 'main_menu')

    else:
        key = callback.data.split(":")[1]
        models = bot_list_result[key]
        add_buttons(builder, models, 'start_use', 'select_model')

    await callback.bot.answer_callback_query(callback.id)
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        reply_markup=builder.as_markup()
    )


@router.callback_query(F.data == "help")
@router.message(Command("help"))
async def help(callback: CallbackQuery):
    #  bot_list = get_bot_list()

    bot_list_response = BotList.BotList(need_execute_local=True).get_response()
    # Сортируем данные по авторам и именам моделей
    sorted_data = sorted(bot_list_response, key=itemgetter("author", "model_name"))

    # Группируем данные по авторам
    bot_list_result = {key: [item["model_name"] for item in group] for key, group in
                    groupby(sorted_data, key=itemgetter("author"))}

    bot_list_text = str()

    for developer, models in bot_list_result.items():
        bot_list_text += f"Разработчик {developer}:\n"
        for model in models:
            bot_list_text += f"- {model}\n"
        bot_list_text += "\n"

    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text='Выбрать модель', callback_data=f"select_model"))
    builder.row(InlineKeyboardButton(text="<- BACK", callback_data='main_menu'))

    await callback.message.answer(
        text=f"{HELP_MESSAGE}\n{bot_list_text}",
        reply_markup=builder.as_markup()
    )
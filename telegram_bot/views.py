from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
# from telegram_bot.handler import Handler
from Bot_X_API.telegram_bot.assets import WELCOME_MESSAGE, HELP_MESSAGE
import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()

# ''' django setup '''
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
# os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
# django.setup()

router = Router()
# handler = Handler()
REGISTERED = False
BOTLIST_API_URL = f"{os.environ.get('LOCALHOST')}/api/v0/bots"


def get_bot_list():
    response = requests.get(BOTLIST_API_URL)

    if response.status_code == 200:
        response = response.json()
    else:
        return {'error': ['core AFK']}

    bot_list = {}
    for i in response['result']:
        if i['status_code'] == 'active':
            if i['author'] in bot_list:
                bot_list[i['author']].append(i['name'])
            else:
                bot_list[i['author']] = [i['name']]

    return bot_list


def add_buttons(builder, items, key_prefix, back_prefix):
    for i in items:
        builder.add(InlineKeyboardButton(text=i, callback_data=f"{key_prefix}:{i}"))
    builder.row(InlineKeyboardButton(text='<- BACK', callback_data=f'{back_prefix}'))


@router.callback_query(F.data == "main_menu")
@router.message(Command("menu", "start"))
async def main_menu(msg: Message | CallbackQuery):
    global REGISTERED
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(text='Модели', callback_data='select_model'))
    builder.row(InlineKeyboardButton(text='Мой Аккаунт', callback_data='account'))
    builder.row(InlineKeyboardButton(text='Помощь', callback_data='help'))

    if isinstance(msg, CallbackQuery):
        await msg.bot.edit_message_reply_markup(
            chat_id=msg.message.chat.id,
            message_id=msg.message.message_id,
            reply_markup=builder.as_markup()
        )
    elif isinstance(msg, Message):
        await msg.answer(
            text=WELCOME_MESSAGE,
            reply_markup=builder.as_markup()
        )


@router.callback_query(F.data.startswith('start_use'))
async def start_use(callback: CallbackQuery):
    selected_model = int(callback.data.split(":")[1]) + 1  # "start_use:{model}" -> ["start_use, "index of model"]
    start_message = "DIALOGUE MODE IS ON!"
    await callback.message.answer(text=f"{start_message}! You have selected a model with number {selected_model}")


@router.callback_query(F.data.startswith("select_model"))
async def select_model(callback: CallbackQuery):
    bot_list = get_bot_list()
    # bot_list = {'1111': ['aaaa', 'bbbb', 'cccc'], '2222': ['dddd', 'ffff']}
    models = []
    builder = InlineKeyboardBuilder()

    if callback.data == 'select_model':
        if len(bot_list) > 1:
            models = list(bot_list)
            add_buttons(builder, models, 'select_model', 'main_menu')

        else:
            key, models = bot_list.popitem()
            add_buttons(builder, models, 'start_use', 'main_menu')

    else:
        key = callback.data.split(":")[1]
        models = bot_list[key]
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
    bot_list = get_bot_list()
    bot_list_text = str()

    for developer, models in bot_list.items():
        bot_list_text += f"Разработчик {developer}:\n"
        for model in models:
            bot_list_text += f"- {model}\n"
        bot_list_text += "\n"

    # models = [
    #     "Gpt-3.5 4k context    ✅",
    #     "Gpt-3.5 16k context  ⛔️",
    #     "Gpt-4 8k context        ⛔️",
    #     "Gpt-4 32k context       ⛔️"
    # ]
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text='Выбрать модель', callback_data=f"select_model"))
    builder.row(InlineKeyboardButton(text="<- BACK", callback_data='main_menu'))

    await callback.message.answer(
        text=f"{HELP_MESSAGE}\n{bot_list_text}",
        reply_markup=builder.as_markup()
    )


@router.callback_query(F.data == "account")
async def account(callback: CallbackQuery):
    builder = InlineKeyboardBuilder().row(InlineKeyboardButton(text="<- BACK", callback_data='main_menu'))
    await callback.message.answer(
        text=f"""
    👨‍💻  Добро пожаловать, {callback.from_user.first_name}!                                   .
        ├ Ваш юзернейм: @{callback.from_user.username}
        ├ Ваш ID: {callback.from_user.id}
        ├ Ваш баланс: 0
        └ Язык бота: Русский
        
💳  Кол-во запросов:
        ├ GPT-3.5 4k: 10/15 
        ├ GPT-3.5 16k: 10/15 
        ├ GPT-4 8k: 10/15 
        ├ GPT-4 32k: 10/15
        """,
        reply_markup=builder.as_markup()
    )


@router.message()
async def free_mode(msg: Message):
    await msg.answer(text="Free mode")
    answer = await start_use(msg.text)
    await msg.answer(text=f"Start_use: {answer}")


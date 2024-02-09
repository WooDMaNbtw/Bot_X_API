import random, string, os, django
from aiogram import Bot, Dispatcher, Router, F, types
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from itertools import groupby
from operator import itemgetter
# from telegram_bot.assets import HELP_MESSAGE, WELCOME_MESSAGE
from .assets import HELP_MESSAGE, WELCOME_MESSAGE

from Bot_X_API.services import Register, Login, BotList, BotDetail, DialogueList
from .assets import router

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
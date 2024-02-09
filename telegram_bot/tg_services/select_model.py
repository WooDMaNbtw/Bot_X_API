import random, string, os, django
from aiogram import Bot, Dispatcher, Router, F, types
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from itertools import groupby
from operator import itemgetter
from services import Register, Login, BotList, BotDetail, DialogueList
from .assets import router


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

    # bot_list_result = {'1111': ['aaaa', 'bbbb', 'cccc'], '2222': ['dddd', 'ffff']}
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
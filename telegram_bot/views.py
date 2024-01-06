import asyncio
import os
from .handler import Handler
from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

API_TOKEN = os.environ['API_TOKEN']
dp = Dispatcher()
user_router = Router()
handler = Handler()

bot = Bot(token=API_TOKEN, parse_mode='HTML')

@user_router.message(Command('ver2'))
async def main_menu(msg: Message):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(
        text='Model',
        callback_data='select_model')
    )
    builder.row(InlineKeyboardButton(
        text='Options',
        callback_data='options')
    )
    builder.row(InlineKeyboardButton(
        text='Start a dialogue',
        callback_data='start_use')
    )
    await msg.answer(
        '========  Выберите пункт меню:  =========',
        reply_markup=builder.as_markup()
    )


@dp.callback_query(F.data == 'start_use')
async def start_use(callback: CallbackQuery):
    text = ('Тут мы делаем запрос к модели. \n'
            'Получаем какое-то приветствие и выдаем его пользователю.')
    await bot.answer_callback_query(callback.id)
    await callback.message.answer(text=text)


@dp.callback_query(F.data == 'select_model')
async def select_chat_model(callback: CallbackQuery) -> None:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text='GPT',
        callback_data='select_model_GPT')
    )
    builder.add(InlineKeyboardButton(
        text='SBER',
        callback_data='select_model_SBER')
    )
    builder.add(InlineKeyboardButton(
        text='YANDEX',
        callback_data='select_model_YANDEX')
    )
    # await msg.answer(
    #     'Выберите модель для дальнейшего диалога:',
    #     reply_markup=builder.as_markup()
    # )
    await bot.answer_callback_query(callback.id)  # Ответ на запрос, чтобы убрать "часики" в кнопке
    await bot.edit_message_reply_markup(chat_id=callback.message.chat.id,
                                        message_id=callback.message.message_id,
                                        # reply_markup=None)  # Очищаем кнопки
                                        reply_markup=builder.as_markup())  # Заменяем кнопки


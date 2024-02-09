import os, django, asyncio, logging
from aiogram import Dispatcher, Bot

import sys
sys.path.append(r'D:\devops\bot-x-tele\Bot_X_API')

''' django setup '''
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Bot_X_API.core.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()

from tg_services.assets import router
from tg_services import help, select_model, start, main_menu


async def main() -> None:
    token: str = os.environ.get('API_TOKEN')
    bot = Bot(token=token, parse_mode='HTML')
    dp = Dispatcher()
    dp.include_router(router=router)
    dp.message.register(start.start)
    dp.message.register(main_menu.main_menu)
    dp.message.register(help.help)
    dp.message.register(select_model.select_model)
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt as ex:
        print("Error: ", ex)
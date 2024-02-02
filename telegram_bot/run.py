import os, django, asyncio, logging
from aiogram import Dispatcher, Bot, F
from views import router
from start import start
from views import main_menu
from help import help
from select_model import select_model
''' django setup '''
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()


async def main() -> None:
    token: str = os.environ.get('API_TOKEN')
    bot = Bot(token=token, parse_mode='HTML')
    dp = Dispatcher()
    dp.include_router(router=router)
    dp.message.register(start)
    dp.message.register(main_menu)
    dp.message.register(help)
    dp.message.register(select_model)
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt as ex:
        print("Error: ", ex)
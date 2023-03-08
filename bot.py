import asyncio

from aiogram import Bot, Dispatcher

from config.config import load_config, Config

from keyboards.main_menu import set_main_menu

from handlers.other_handlers import register_other_handlers

from handlers.user_handlers import register_user_commands

def register_all_handlers(dp: Dispatcher) -> None:
    register_user_commands(dp)
    register_other_handlers(dp)

async def main():
    config:Config = load_config()
    bot: Bot = Bot(token = config.tg_bot.token, parse_mode='HTML')
    dp:Dispatcher = Dispatcher(bot)

    await set_main_menu(dp)
    register_all_handlers(dp)
    try:
        await dp.start_polling()
    except:
        await bot.close()


if __name__ == '__main__':
    asyncio.run(main())

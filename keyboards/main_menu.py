from aiogram import Dispatcher, types
from lexicon.lexicon import LEXICON_MENU


async def set_main_menu(dp:Dispatcher) -> None:
    main_menu_commands = [types.BotCommand(command=command, description=desc) for command, desc in LEXICON_MENU.items()]
    await dp.bot.set_my_commands(main_menu_commands)
from aiogram.types import Message
from aiogram import Dispatcher
from lexicon.lexicon import LEXICON

async def process_other_message(message:Message) -> None:
    await message.answer(LEXICON['other_message'])


def register_other_handlers(dp:Dispatcher) -> None:
    dp.register_message_handler(process_other_message)
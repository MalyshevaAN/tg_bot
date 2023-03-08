from lexicon.lexicon import LEXICON
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def create_pg_kb(*buttons: str) -> InlineKeyboardMarkup:
    pg_kb: InlineKeyboardMarkup = InlineKeyboardMarkup()
    pg_kb.row(*[InlineKeyboardButton(LEXICON[button] if buttons in LEXICON else button, callback_data=button) for button in buttons])
    return pg_kb

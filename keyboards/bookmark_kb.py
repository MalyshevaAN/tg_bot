from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from services.file_handling import book_pages
from lexicon.lexicon import LEXICON



def create_bookmark_kb(*pages:int) -> InlineKeyboardMarkup:
    bookmark_kb:InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
    if pages:
        bookmark_kb.add(*[InlineKeyboardButton(f'{page}-{book_pages[page][:100]}...', callback_data=str(page)) for page in pages])

    bookmark_kb.add(InlineKeyboardButton(text=LEXICON['edit_bookmarks_button'], callback_data='edit_bookmarks'), InlineKeyboardButton(text=LEXICON['cancel'], callback_data='cancel'))
    return bookmark_kb

def edit_bookmark_kb(*pages:int) -> InlineKeyboardMarkup:
    edit_kb: InlineKeyboardMarkup = InlineKeyboardMarkup()
    buttons = [InlineKeyboardButton(text = f'{LEXICON["del"]} {page}-{book_pages[page][:100]}...',callback_data = f'del{page}') for page in pages]
    edit_kb.add(*buttons)
    edit_kb.add(InlineKeyboardButton(text=LEXICON['cancel'], callback_data='cancel'))
    return edit_kb

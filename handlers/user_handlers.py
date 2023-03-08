from copy import deepcopy
from database.database import database, users_db
from aiogram.types import Message, InlineKeyboardMarkup, CallbackQuery
from aiogram import Dispatcher
from lexicon.lexicon import LEXICON
from services.file_handling import book_pages
from keyboards.pagination import create_pg_kb
from keyboards.bookmark_kb import create_bookmark_kb, edit_bookmark_kb


async def process_start_command(message:Message) -> None:
    id = message.from_user.id
    if not (id in users_db):
        users_db[id] = deepcopy(database)
    await message.answer(LEXICON['/start'])


async def process_help_command(message:Message) -> None:
    await message.answer(LEXICON['/help'])

async def process_cancel_command(message:Message) -> None:
    await message.answer(LEXICON['/cancel'])


async def process_beginning_command(message:Message) -> None:
    users_db[message.from_user.id]['current_page'] = 1
    kb:InlineKeyboardMarkup = create_pg_kb('1',f'{users_db[message.from_user.id]["current_page"]}/{len(book_pages)}','forward')
    await message.answer(text=book_pages[users_db[message.from_user.id]['current_page']], reply_markup=kb)

async def process_continue_command(message:Message) -> None:
    page = users_db[message.from_user.id]['current_page']
    kb: InlineKeyboardMarkup = create_pg_kb('back', f'{page}/{len(book_pages)}','forward')
    await message.answer(text=book_pages[page], reply_markup=kb)


async def process_bookmarks_command(message:Message) -> None:
    bookmarks:set = users_db[message.from_user.id]['bookmarks']

    if bookmarks:
        text = LEXICON['/bookmarks']
        kb = create_bookmark_kb(*bookmarks)
        await message.answer(text=text, reply_markup=kb)
    else:
        await message.answer(LEXICON['no_bookmarks'])

async def process_forward_call(callback: CallbackQuery) -> None:
    if users_db[callback.from_user.id]['current_page'] < len(book_pages):
        users_db[callback.from_user.id]['current_page'] += 1
        page = users_db[callback.from_user.id]['current_page']
        text = book_pages[page]
        kb: InlineKeyboardMarkup = create_pg_kb('back', f'{page}/{len(book_pages)}', 'forward')
        await callback.message.edit_text(text=text, reply_markup=kb)
    else:
        await callback.message.edit_text(text=LEXICON['end'])
    await callback.answer()

async def process_back_call(callback: CallbackQuery) -> None:
    if users_db[callback.from_user.id]['current_page'] > 1:
        users_db[callback.from_user.id]['current_page'] -= 1
        page = users_db[callback.from_user.id]['current_page']
        text = book_pages[page]
        kb: InlineKeyboardMarkup = create_pg_kb('back', f'{page}/{len(book_pages)}', 'forward')
        await callback.message.edit_text(text=text, reply_markup=kb)
    await callback.answer()

async def process_page_call(callback:CallbackQuery) -> None:
    users_db[callback.from_user.id]['bookmarks'].add(users_db[callback.from_user.id]['current_page'])
    await callback.answer(text=LEXICON['add_bookmark'])

async def process_bookmark_open(callback: CallbackQuery) -> None:
    page = int(callback.data)
    users_db[callback.from_user.id]['current_page'] = page
    text = book_pages[page]
    kb: InlineKeyboardMarkup = create_pg_kb('back', f'{page}/{len(book_pages)}', 'forward')
    await callback.message.edit_text(text=text, reply_markup=kb)
    await callback.answer()

async def process_edit_press(callback: CallbackQuery) -> None:
    text = LEXICON['edit_bookmarks_button']
    kb: InlineKeyboardMarkup = edit_bookmark_kb(*users_db[callback.from_user.id]['bookmarks'])
    await callback.message.edit_text(text=text, reply_markup=kb)


async def process_cancel_press(callback: CallbackQuery) -> None:
    await callback.message.edit_text(LEXICON['cancel_text'])
    await callback.answer()

async def process_press_delete_bookmark(callback:CallbackQuery) -> None:
    users_db[callback.from_user.id]['bookmarks'].remove(int(callback.data[3:]))
    if users_db[callback.from_user.id]['bookmarks']:
        text = LEXICON['edit_bookmarks_button']
        kb: InlineKeyboardMarkup = edit_bookmark_kb(*users_db[callback.from_user.id]['bookmarks'])
        await callback.message.edit_text(text = text, reply_markup=kb)
    else:
        await callback.message.edit_text(text=LEXICON['no_bookmarks'])

    await callback.answer()



def register_user_commands(dp:Dispatcher) -> None:
    dp.register_message_handler(process_start_command, commands='start')
    dp.register_message_handler(process_help_command, commands = 'help')
    dp.register_message_handler(process_cancel_command, commands = 'cancel')
    dp.register_message_handler(process_beginning_command, commands = 'beginning')
    dp.register_message_handler(process_continue_command, commands='continue')
    dp.register_message_handler(process_bookmarks_command, commands = 'bookmarks')
    dp.register_callback_query_handler(process_forward_call, text = 'forward')
    dp.register_callback_query_handler(process_back_call, text='back')
    dp.register_callback_query_handler(process_page_call, lambda x: '/' in x.data and x.data.replace('/','').isdigit())
    dp.register_callback_query_handler(process_bookmark_open, lambda x: x.data.isdigit())
    dp.register_callback_query_handler(process_edit_press, text='edit_bookmarks')
    dp.register_callback_query_handler(process_cancel_press, text='cancel')
    dp.register_callback_query_handler(process_press_delete_bookmark, lambda x: x.data[:3] == 'del' and x.data[3:].isdigit())

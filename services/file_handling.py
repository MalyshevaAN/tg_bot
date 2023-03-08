import codecs

BOOK_PATH = 'E:\учеба\python_tg\BookBot\\book\\book.txt'
PAGE_SIZE = 1050

book_pages: dict[int, str] = {}

def _get_part_text(text:str, start:int, page_size:int) -> tuple[str, int]:
    signs = [',', '.', '!', ':', ';', '?']
    end_of_page = min(len(text)-1, start + page_size-1)
    if end_of_page == len(text) - 1:
        return text[start:len(text)], len(text)-start
    for i in range(end_of_page, start, -1):
        if text[i] in signs and text[i]+ text[i+1] != '..' and text[i+1] + text[i+2] != '..':
            break
    return text[start:i+1], i-start+1


def prepare_book(path:str) -> None:
    file = codecs.open(path, 'r', 'utf-8')
    text = file.read()
    page_number = 1
    start_index = 0
    whole_length = 0
    while whole_length != len(text):
        current_text, current_length = _get_part_text(text, start_index, PAGE_SIZE)
        book_pages[page_number] = current_text.lstrip('     \n\v\f\r')
        whole_length += current_length
        page_number += 1
        start_index += current_length



prepare_book(BOOK_PATH)







prepare_book(BOOK_PATH)
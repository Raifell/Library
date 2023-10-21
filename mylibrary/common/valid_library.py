import datetime
import re
from library.models import Book, Reader


def valid_book(qery):
    """Проверка название: буквы + пробел + цифры + тире
    Проверка имя + фамилия + жанр: буквы + пробел + тире
    Проверка год публикации: диапазон 1900-2023
    Проверка количество страниц: если поле заполнено"""

    valid = True
    pattern_title = lambda x: bool(re.compile(r'[a-zA-Zа-яА-ЯйЙёЁ\s0-9-]').match(x))
    pattern_other = lambda x: bool(re.compile(r'[a-zA-Zа-яА-ЯйЙёЁ\s-]').match(x))
    for book_desc_value in qery[:4]:
        if book_desc_value:
            for index in book_desc_value:
                if valid:
                    valid = pattern_title(index) if book_desc_value == qery[0] else pattern_other(index)
        else:
            valid = False
            break

    if qery[4].isdigit():
        if int(qery[4]) < 1900 or int(qery[4]) > 2023:
            valid = False
    else:
        valid = False

    if not qery[5]:
        valid = False
    return valid


def valid_reader(qery):
    """Проверка имя + фамилия: буквы + пробел + тире
    Проверка возраст: диапазон 5-90"""

    valid = True
    for reader_param in [*qery[:2]]:
        if reader_param:
            for index in reader_param:
                if valid:
                    valid = bool(re.compile(r'[a-zA-Zа-яА-ЯйЙёЁ\s-]').match(index))
        else:
            valid = False
            break
    if int(qery[2]) < 5 or int(qery[2]) > 90:
        valid = False
    return valid


def valid_rent(qery):
    """Проверка название книги: если в списке названий книг
    Проверка фамилии: если в списке фамилий
    Проверка даты: если поля заполнены + если дата возврата позже даты получения"""

    valid = 'clear'
    books = [book_title for dict_ in Book.objects.values('title') for book_title in dict_.values()]
    users = [user_surname for dict_ in Reader.objects.values('surname') for user_surname in dict_.values()]
    if qery[0] not in books:
        return 'book_error'
    if qery[1] not in users:
        return 'user_error'
    if qery[2] and qery[3]:
        start = datetime.datetime.strptime(qery[2], '%Y-%m-%d').date()
        end = datetime.datetime.strptime(qery[3], '%Y-%m-%d').date()
        if start >= end:
            return 'time_error'
    else:
        return 'time_error'
    return valid

import datetime
import re
from django.shortcuts import render
from .models import Book, Reader, BookRent


# Create your views here.
def show_start_page(request):
    return render(request, "index.html")


###################### Show,Valid,Add - Book #########################

def show_showbooks_page(request):
    if request.method == "POST":
        if 'delete' in request.POST:
            Book.objects.filter(title=request.POST['delete']).delete()

    context = {'books': Book.objects.all()}

    return render(request, "showBooks.html", context=context)


def valid_book(qery):
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
    return valid


def show_addbook_page(request):
    data = False
    update = False
    valid = True
    book_action = None
    if request.method == "POST":
        if 'add_book' in request.POST:
            new_book = request.POST.getlist('add_book')
            if new_book[5]:
                valid = valid_book(new_book)
                if valid:
                    book_action = 'new'
                    Book.objects.create(title=new_book[0],
                                        author_name=new_book[1],
                                        author_surname=new_book[2],
                                        genre=new_book[3],
                                        publication_year=new_book[4],
                                        page_count=new_book[5],
                                        description=new_book[6])
            else:
                valid = False
        elif 'update' in request.POST:
            data = Book.objects.get(id=request.POST['update'])
            update = True
        elif 'update_book' in request.POST:
            up_book_value = request.POST.getlist('update_book')
            if up_book_value[5]:
                valid = valid_book(up_book_value)
                if valid:
                    book_action = 're_new'
                    Book.objects.filter(id=up_book_value[7]).update(title=up_book_value[0],
                                                                    author_name=up_book_value[1],
                                                                    author_surname=up_book_value[2],
                                                                    genre=up_book_value[3],
                                                                    publication_year=up_book_value[4],
                                                                    page_count=up_book_value[5],
                                                                    description=up_book_value[6])

            else:
                valid = False

    return render(request, "addBook.html", {'data': data, 'update': update, 'valid': valid, 'book_action': book_action})


###################### Show,Valid,Add - Readers #########################

def show_readers(request):
    if request.method == "POST":
        if 'delete' in request.POST:
            Reader.objects.filter(id=request.POST['delete']).delete()

    context = {'readers': Reader.objects.all()}
    return render(request, 'showreaders.html', context=context)


def valid_reader(qery):
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


def show_addreader_page(request):
    data = False
    update = False
    valid = True
    reader_action = None
    if request.method == "POST":
        if 'add_reader' in request.POST:
            new_reader = request.POST.getlist('add_reader')
            valid = valid_reader(new_reader)
            if valid:
                reader_action = 'new'
                Reader.objects.create(name=new_reader[0],
                                      surname=new_reader[1],
                                      age=new_reader[2],
                                      address=new_reader[3])
        elif 'update' in request.POST:
            data = Reader.objects.get(id=request.POST['update'])
            update = True
        elif 'update_reader' in request.POST:
            update_reader = request.POST.getlist('update_reader')
            valid = valid_reader(update_reader)
            if valid:
                reader_action = 're_new'
                Reader.objects.filter(id=update_reader[4]).update(name=update_reader[0],
                                                                  surname=update_reader[1],
                                                                  age=update_reader[2],
                                                                  address=update_reader[3])

    return render(request, "addReader.html", {'data': data, 'update': update, 'valid': valid, 'reader_action': reader_action})


###################### Show,Valid,Add - Rent #########################

def show_rents(request):
    if request.method == "POST":
        if 'delete' in request.POST:
            BookRent.objects.filter(id=request.POST['delete']).delete()

    context = {'rents': BookRent.objects.all()}
    return render(request, 'showrents.html', context=context)


def valid_rent(qery):
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


def show_addrent_page(request):
    data = False
    update = False
    valid = 'clear'
    rent_action = None
    if request.method == "POST":
        if 'add_rent' in request.POST:
            new_rent = request.POST.getlist('add_rent')
            valid = valid_rent(new_rent)

            if valid == 'clear':
                rent_action = 'new'
                BookRent.objects.create(book_title=new_rent[0],
                                        reader_surname=new_rent[1],
                                        rent_date=new_rent[2],
                                        return_date=new_rent[3])
        elif 'update' in request.POST:
            data = BookRent.objects.get(id=request.POST['update'])
            data.rent_date = str(data.rent_date)
            data.return_date = str(data.return_date)
            update = True
        elif 'update_rent' in request.POST:
            update_rent = request.POST.getlist('update_rent')
            valid = valid_rent(update_rent)
            if valid == 'clear':
                rent_action = 're_new'
                BookRent.objects.filter(id=update_rent[4]).update(book_title=update_rent[0],
                                                                  reader_surname=update_rent[1],
                                                                  rent_date=update_rent[2],
                                                                  return_date=update_rent[3])

    return render(request, "addRent.html", {'data': data, 'update': update, 'valid': valid, 'rent_action': rent_action})

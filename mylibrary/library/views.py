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


def show_addrent_page(request):
    if request.method == "POST":
        title = request.POST.get("book_title")
        reader = request.POST.get("reader_surname")
        rent_date = request.POST.get("rent_date")
        return_date = request.POST.get("return_date")

        if rent_date and return_date:
            BookRent.objects.create(book_title=title,
                                    reader_surname=reader,
                                    rent_date=rent_date,
                                    return_date=return_date)

    return render(request, "addRent.html")


def show_rents(request):
    context = {'rents': BookRent.objects.all()}
    return render(request, 'showrents.html', context=context)

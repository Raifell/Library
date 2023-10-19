import re
from django.shortcuts import render
from .models import Book, Reader, BookRent


# Create your views here.
def show_start_page(request):
    return render(request, "index.html")


def show_showbooks_page(request):
    if request.method == "POST":
        if 'delete' in request.POST:
            Book.objects.filter(title=request.POST['delete']).delete()

    context = {'books': Book.objects.all()}

    return render(request, "showBooks.html", context=context)


def valid_book(qery):
    valid = True
    for book_desc_value in qery[:4]:
        if book_desc_value:
            for index in book_desc_value:
                if valid:
                    valid = bool(re.compile(r'[a-zA-Zа-яА-ЯйЙёЁ]').match(index))

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
            update = 'update'
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


def show_addreader_page(request):
    if request.method == "POST":
        name = request.POST.get("reader_name")
        surname = request.POST.get("reader_surname")
        age = request.POST.get("reader_age")
        address = request.POST.get("reader_address")

        if age:
            Reader.objects.create(name=name,
                                  surname=surname,
                                  age=age,
                                  address=address)

    return render(request, "addReader.html")


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


def show_readers(request):
    context = {'readers': Reader.objects.all()}
    return render(request, 'showreaders.html', context=context)


def show_rents(request):
    context = {'rents': BookRent.objects.all()}
    return render(request, 'showrents.html', context=context)

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

    return valid
    pass


def show_addbook_page(request):
    data = False
    update = False
    valid = True
    if request.method == "POST":
        if 'add_book' in request.POST:
            new_book = request.POST.getlist('add_book')
            if new_book[5]:
                valid_book(new_book)
                # Book.objects.create(title=new_book[0],
                #                     author_name=new_book[1],
                #                     author_surname=new_book[2],
                #                     genre=new_book[3],
                #                     publication_year=new_book[4],
                #                     page_count=new_book[5],
                #                     description=new_book[6])
        elif 'update' in request.POST:
            data = Book.objects.get(id=request.POST['update'])
            update = 'update'
        elif 'update_book' in request.POST:
            up_book_value = request.POST.getlist('update_book')
            Book.objects.filter(id=up_book_value[7]).update(title=up_book_value[0],
                                                            author_name=up_book_value[1],
                                                            author_surname=up_book_value[2],
                                                            genre=up_book_value[3],
                                                            publication_year=up_book_value[4],
                                                            page_count=up_book_value[5],
                                                            description=up_book_value[6])

    return render(request, "addBook.html", {'data': data, 'update': update, 'valid': valid})


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

from django.shortcuts import render
from .models import Book, Reader, BookRent
from common import valid_library as vl
from common import commit_library as cl


# Create your views here.
def show_start_page(request):
    return render(request, "index.html")


###################### Show,Add - Book #########################

def show_showbooks_page(request):
    if request.method == "POST":
        if 'delete' in request.POST:
            Book.objects.filter(title=request.POST['delete']).delete()

    return render(request, "showBooks.html", {'books': Book.objects.all()})


def show_addbook_page(request):
    data, update, valid, book_action = False, False, True, None

    if request.method == "POST":
        if 'add_book' in request.POST:
            new_book = request.POST.getlist('add_book')
            valid = vl.valid_book(new_book)
            if valid:
                book_action = 'new'
                cl.add_book(new_book)

        elif 'update' in request.POST:
            data = Book.objects.get(id=request.POST['update'])
            update = True

        elif 'update_book' in request.POST:
            update_book = request.POST.getlist('update_book')
            valid = vl.valid_book(update_book)
            if valid:
                book_action = 're_new'
                cl.update_book(update_book)

    return render(request, "addBook.html", {'data': data, 'update': update, 'valid': valid, 'book_action': book_action})


###################### Show,Add - Readers #########################

def show_readers(request):
    if request.method == "POST":
        if 'delete' in request.POST:
            Reader.objects.filter(id=request.POST['delete']).delete()

    return render(request, 'showreaders.html', {'readers': Reader.objects.all()})


def show_addreader_page(request):
    data, update, valid, reader_action = False, False, True, None

    if request.method == "POST":
        if 'add_reader' in request.POST:
            new_reader = request.POST.getlist('add_reader')
            valid = vl.valid_reader(new_reader)
            if valid:
                reader_action = 'new'
                cl.add_reader(new_reader)

        elif 'update' in request.POST:
            data = Reader.objects.get(id=request.POST['update'])
            update = True

        elif 'update_reader' in request.POST:
            update_reader = request.POST.getlist('update_reader')
            valid = vl.valid_reader(update_reader)
            if valid:
                reader_action = 're_new'
                cl.update_reader(update_reader)

    return render(request, "addReader.html", {'data': data, 'update': update, 'valid': valid, 'reader_action': reader_action})


###################### Show,Add - Rent #########################

def show_rents(request):
    if request.method == "POST":
        if 'delete' in request.POST:
            BookRent.objects.filter(id=request.POST['delete']).delete()

    return render(request, 'showrents.html', {'rents': BookRent.objects.all()})


def show_addrent_page(request):
    data, update, valid, rent_action = False, False, 'clear', None

    if request.method == "POST":
        if 'add_rent' in request.POST:
            new_rent = request.POST.getlist('add_rent')
            valid = vl.valid_rent(new_rent)
            if valid == 'clear':
                rent_action = 'new'
                cl.add_rent(new_rent)

        elif 'update' in request.POST:
            data = BookRent.objects.get(id=request.POST['update'])
            data.rent_date = str(data.rent_date)
            data.return_date = str(data.return_date)
            update = True

        elif 'update_rent' in request.POST:
            update_rent = request.POST.getlist('update_rent')
            valid = vl.valid_rent(update_rent)
            if valid == 'clear':
                rent_action = 're_new'
                cl.update_rent(update_rent)

    return render(request, "addRent.html", {'data': data, 'update': update, 'valid': valid, 'rent_action': rent_action})

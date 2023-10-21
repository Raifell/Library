from library.models import Book, Reader, BookRent

# Book operations


def add_book(li: list):
    Book.objects.create(title=li[0],
                        author_name=li[1],
                        author_surname=li[2],
                        genre=li[3],
                        publication_year=li[4],
                        page_count=li[5],
                        description=li[6])


def update_book(li: list):
    Book.objects.filter(id=li[7]).update(title=li[0],
                                         author_name=li[1],
                                         author_surname=li[2],
                                         genre=li[3],
                                         publication_year=li[4],
                                         page_count=li[5],
                                         description=li[6])


# Reader operations


def add_reader(li: list):
    Reader.objects.create(name=li[0],
                          surname=li[1],
                          age=li[2],
                          address=li[3])


def update_reader(li: list):
    Reader.objects.filter(id=li[4]).update(name=li[0],
                                           surname=li[1],
                                           age=li[2],
                                           address=li[3])


# Rent operations


def add_rent(li: list):
    BookRent.objects.create(book_title=li[0],
                            reader_surname=li[1],
                            rent_date=li[2],
                            return_date=li[3])


def update_rent(li: list):
    BookRent.objects.filter(id=li[4]).update(book_title=li[0],
                                             reader_surname=li[1],
                                             rent_date=li[2],
                                             return_date=li[3])

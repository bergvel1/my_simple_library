from django_filters import FilterSet

from catalog.models import Author, Book, BookInstance


class AuthorFilter(FilterSet):
    class Meta:
        model = Author
        strict = False
        fields = {
            "first_name": ["icontains"],
            "last_name": ["icontains"]
        }


class BookFilter(FilterSet):
    class Meta:
        model = Book
        fields = {
            "title": ["icontains"],
            "author__first_name": ["icontains"],
            "author__last_name": ["icontains"],
            "isbn": ["iexact"]
        }


class BookInstanceFilter(FilterSet):
    class Meta:
        model = BookInstance
        fields = {
            "book__title": ["icontains"],
            "book__author__first_name": ["icontains"],
            "book__author__last_name": ["icontains"],
            "book__isbn": ["iexact"],
            "id": ["iexact"]
        }

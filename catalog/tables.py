import django_tables2 as tables
from django_tables2 import views

from catalog.models import Author


class AuthorTable(tables.Table):
    author = tables.Column(empty_values=(), linkify=lambda record: record.get_absolute_url(),
                           order_by=('last_name', 'first_name'))
    date_of_birth = tables.Column()
    date_of_death = tables.Column()

    class Meta:
        empty_text = 'No authors found'
        template_name = 'django_tables2/bootstrap4.html'

    def render_author(self, record):
        return '{}, {}'.format(record.last_name, record.first_name)


class BookTable(tables.Table):
    title = tables.Column(linkify=True)
    author = tables.Column(linkify=True)
    genre = tables.ManyToManyColumn(transform=lambda genre: genre.name)

    isbn = tables.Column()

    class Meta:
        empty_text = 'No books found'
        template_name = 'django_tables2/bootstrap4.html'


class BookInstanceTable(tables.Table):
    title = tables.Column(linkify=True, accessor='book')
    author = tables.Column(linkify=True, accessor='book.author')
    id = tables.Column()
    isbn = tables.Column(accessor='book.isbn')
    due_back = tables.Column()
    borrower = tables.Column()

    class Meta:
        empty_text = 'No books found'
        template_name = 'django_tables2/bootstrap4.html'

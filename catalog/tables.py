import django_tables2 as tables


class AuthorTable(tables.Table):
    author = tables.Column(empty_values=(), linkify=lambda record: record.get_absolute_url(),
                           order_by=('last_name', 'first_name'))
    date_of_birth = tables.Column()
    date_of_death = tables.Column()

    class Meta:
        title = 'Authors'
        placeholder = 'Search authors'
        empty_text = 'No authors found'
        template_name = 'mybootstrap4.html'
        attrs = {'id': 'author_table'}

    def render_author(self, record):
        return '{}, {}'.format(record.last_name, record.first_name)


class BookTable(tables.Table):
    title = tables.Column(linkify=True)
    author = tables.Column(linkify=True)
    genre = tables.ManyToManyColumn(transform=lambda genre: genre.name)

    isbn = tables.Column()

    class Meta:
        title = 'Books'
        placeholder = 'Search books'
        empty_text = 'No books found'
        template_name = 'mybootstrap4.html'
        attrs = {'id': 'book_table'}


class BookInstanceTable(tables.Table):
    title = tables.Column(linkify=True, accessor='book')
    author = tables.Column(linkify=True, accessor='book.author')
    id = tables.Column()
    isbn = tables.Column(accessor='book.isbn')
    due_back = tables.Column()
    borrower = tables.Column()

    class Meta:
        placeholder = 'Search books'
        empty_text = 'No books found'
        template_name = 'mybootstrap4.html'
        attrs = {'id': 'bookinstance_table'}

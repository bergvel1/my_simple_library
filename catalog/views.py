from django.shortcuts import render
from django_filters.views import FilterView

from catalog.models import Book, Author, BookInstance, Genre
from catalog.filters import AuthorFilter, BookFilter, BookInstanceFilter


def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

from django.views import generic


class BookDetailView(generic.DetailView):
    model = Book


class AuthorDetailView(generic.DetailView):
    model = Author


from django.contrib.auth.mixins import PermissionRequiredMixin

import datetime

from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from catalog.forms import RenewBookForm


@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed'))

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)


from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


class AuthorCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'catalog.can_mark_returned'
    model = Author
    fields = '__all__'
    initial = {'date_of_death': '05/01/2018'}


class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'catalog.can_mark_returned'
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']


class AuthorDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'catalog.can_mark_returned'
    model = Author
    success_url = reverse_lazy('authors')


class BookCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'catalog.can_mark_returned'
    model = Book
    fields = '__all__'


class BookUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'catalog.can_mark_returned'
    model = Book
    fields = '__all__'


class BookDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'catalog.can_mark_returned'
    model = Book
    success_url = reverse_lazy('books')

from .tables import AuthorTable, BookTable, BookInstanceTable
from django_tables2 import RequestConfig, SingleTableMixin


def authors(request):
    table = AuthorTable(Author.objects.all())
    f = AuthorFilter(request.GET, queryset=Author.objects.all())
    RequestConfig(request, paginate={'per_page': 10}).configure(table)
    return render(request, 'catalog/authors.html', {'authors': table, 'is_paginated': table.paginator.num_pages > 1, 'filter': f})


def books(request):
    table = BookTable(Book.objects.all())
    f = BookFilter(request.GET, queryset=Book.objects.all())
    RequestConfig(request, paginate={'per_page': 10}).configure(table)
    return render(request, 'catalog/books.html', {'books': table, 'is_paginated': table.paginator.num_pages > 1, 'filter': f})

@login_required
def mybooks(request):
    my_borrowed_list = BookInstance.objects.filter(borrower=request.user).filter(status__exact='o').order_by('due_back')
    table = BookInstanceTable(my_borrowed_list)
    f = BookInstanceFilter(request.GET, queryset=my_borrowed_list)
    RequestConfig(request, paginate={'per_page': 10}).configure(table)
    return render(request, 'catalog/bookinstance_list_borrowed_user.html', {'mybooks': table, 'is_paginated': table.paginator.num_pages > 1, 'filter': f})


@permission_required('catalog.can_mark_returned')
def all_borrowed_books(request):
    all_borrowed_list = BookInstance.objects.filter(status__exact='o').order_by('due_back')
    table = BookInstanceTable(all_borrowed_list)
    f = BookInstanceFilter(request.GET, queryset=all_borrowed_list)
    RequestConfig(request, paginate={'per_page': 10}).configure(table)
    return render(request, 'catalog/bookinstance_list_borrowed_all.html', {'borrowedbooks': table, 'is_paginated': table.paginator.num_pages > 1, 'filter': f})


class FilteredAuthorListView(SingleTableMixin, FilterView):
    table_class = AuthorTable
    model = Author
    template_name = "catalog/authors.html"

    filterset_class = AuthorFilter


class FilteredBookListView(SingleTableMixin, FilterView):
    table_class = BookTable
    model = Book
    template_name = "catalog/books.html"

    filterset_class = BookFilter


class FilteredBookInstanceListView(SingleTableMixin, FilterView):
    table_class = BookInstanceTable
    model = BookInstance
    #template_name = "catalog/books.html"

    filterset_class = BookInstanceFilter

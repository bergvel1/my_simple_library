from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.books, name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/', views.authors, name='authors'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    path('mybooks/', views.mybooks, name='my-borrowed'),
    path('allbooks/', views.all_borrowed_books, name='all-borrowed'),
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
    path('author/create/', views.AuthorCreate.as_view(), name='author_create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author_update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author_delete'),
    path('book/create/', views.BookCreate.as_view(), name='book_create'),
    path('book/<int:pk>/update/', views.BookUpdate.as_view(), name='book_update'),
    path('book/<int:pk>/delete/', views.BookDelete.as_view(), name='book_delete'),
]
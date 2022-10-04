from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from .models import Author, Book, BookInstance, Genre

def demo(request):
    return HttpResponse("hello ashiti")

def index(request):

    num_books = Book.objects.count()
    num_bookInstance = BookInstance.objects.count()

    # available books
    ava_books  = BookInstance.objects.filter(status__exact='A')
    num_ava_books = ava_books.count()
    num_genre = Genre.objects.count()
    context = {
        "num_books": num_books,
        "num_bookIstance": num_bookInstance,
        "available_book": num_ava_books,
        "num_genre": num_genre
    }

    return render(request, "catalog/index.html", context)


class BookListView(ListView):
    '''  '''

    model = Book
    templates_name = "catalog/book_list.html"
    context_object_name = "books"
    extra_context = {"title": "List of books"}

    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        context['new_data'] = "this a sample of data"
        return context

class BookDetailView(DetailView):
    
    model = Book
    template_name = 'catalog/book_detail.html'
    extra_context = {"title": "Detail book"}
    

class AuthorListView(ListView):

    model = Author
    template_name = "catalog/authors_list.html"
    context_object_name = "authors"
    extra_context = {"title": "Authors list"}
        
class AuthorDetailView(DetailView):

    model = Author
    template_name = 'catalog/author_detail.html'
    extra_context = {"title": "Author detail"}

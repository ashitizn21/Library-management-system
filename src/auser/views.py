from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Author

class AuthorListView(ListView):

    model = Author
    template_name = "auser/authors_list.html"
    context_object_name = "authors"
    extra_context = {"title": "Authors list"}
        
class AuthorDetailView(DetailView):

    model = Author
    template_name = 'auser/author_detail.html'
    extra_context = {"title": "Author detail"}

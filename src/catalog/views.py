from urllib import response
from django.shortcuts import render, get_object_or_404
from django.http import  HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required, permission_required
import datetime
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.db.models import Q

from auser.models import User
from .models import Author, Book, BookInstance, Genre
from .forms import RenewBookForm


# def demo(request):
#     return HttpResponse("hello ashiti")

def index(request):

    num_books = Book.objects.count()
    num_bookInstance = BookInstance.objects.count()

    # available books
    ava_books  = BookInstance.objects.filter(status__exact='A')
    num_ava_books = ava_books.count()
    num_genre = Genre.objects.count()


    # Get a session value by its key (e.g. 'my_car'), raising a KeyError if the key is not present
    # my_car = request.session['my_car']

    # Get a session value, setting a default if it is not present ('mini')
    # my_car = request.session.get('my_car', 'mini')

    # Set a session value
    # request.session['my_car'] = 'mini'
    # del request.session['my_car']
    # my_car = request.session.get('my_car')
    # print(my_car)
    # Delete a session value
    # del request.session['my_car']

    # --- counting how many times this user visit the site
    num_visit = request.session.get("visit_no", 0)
    request.session["visit_no"] = num_visit + 1


    context = {
        "num_books": num_books,
        "num_bookIstance": num_bookInstance,
        "available_book": num_ava_books,
        "num_genre": num_genre,
        "user_visit_no": num_visit
    }

    return render(request, "catalog/index.html", context)


class BookListView(ListView):
    '''  '''

    model = Book
    templates_name = "catalog/book_list.html"
    context_object_name = "books"
    extra_context = {"title": "List of books"}
    paginate_by = 3
    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        context['new_data'] = "this a sample of data"
        return context

class BookDetailView(DetailView):
    
    model = Book
    template_name = 'catalog/book_detail.html'
    extra_context = {"title": "Detail book"}
    
class LoanedBooksByUserListView(LoginRequiredMixin, ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'catalog/loan_book/i_borrowed_list.html'
    extra_context = {"title": "Loaned book"}
    context_object_name = "borrowed_books"
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__iexact='O').order_by('due_back')


@login_required
@permission_required("catalog.can_mark_returns", raise_exception=True)
def RenewDateBookView(request, pk):
    ''' Renewal due date of book view (function based view)  '''
    print("SINPER", pk)
    book_instance = get_object_or_404(BookInstance, pk=pk)
    
    if request.method == "POST" :
        form = RenewBookForm(request.POST)
        if form.is_valid():
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            return  HttpResponseRedirect(reverse_lazy("catalog:loaned_book"))
    else:
        default_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={"renewal_date": default_date })
    

    context = {
        "form": form,
        "book_instance": book_instance,
    }

    return render(request, "catalog/loan_book/renew.html", context)


# class RenewDueDateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
#     ''' Renewal due date of book view (class based) '''
#     model = BookInstance
#     form_class = RenewBookForm
#     template_name = "catalog/loan/renew.html"
#     permission_required = ("catalog.can_mark_returns")
#     success_message = _("Due back date is renewed successfully!.")
#     http_method_names = ["post"]

#     def get_queryser(self):
#         return super().get_queryset().filter(id__exact=self.kwargs["id"])
    
#     def form_valid(self, form):
#         response = super().form_valid(form)
#         self.object.due_back = form.cleaned_data['renewal_date']
#         self.object.save()
#         return response
    
class ListLoanedBookView(PermissionRequiredMixin, ListView):
    '''  '''
    model = BookInstance
    permission_required = ("catalog.can_mark_returns",)
    template_name = "catalog/loan_book/list.html"
    context_object_name = "loan_books"
    extra_context = {"title": _("List loaned book")}

    def get_queryset(self):
        return super().get_queryset().exclude(borrower__isnull=True).filter(
            Q(status__iexact='O')
            | Q(status__iexact='R'))
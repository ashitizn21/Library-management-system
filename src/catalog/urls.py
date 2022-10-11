from django.urls import re_path

from . import views

app_name = 'catalog'

urlpatterns = [
    # re_path(r'^$', views.demo, name='demo'),
    re_path(r'^$', views.index, name="index"),
    re_path(r'^books/$', views.BookListView.as_view(), name='list_book'),
    re_path(r'^book/(?P<pk>\d+)/$', views.BookDetailView.as_view(), name='book_detail'),
    re_path(r"^mybooks/$", views.LoanedBooksByUserListView.as_view(), name='loaned_book'),    
]
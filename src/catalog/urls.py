from django.urls import re_path

from . import views

app_name = 'catalog'

urlpatterns = [
    # re_path(r'^$', views.demo, name='demo'),
    re_path(r'^$', views.index, name="index"),
    re_path(r'^books/', views.BookListView.as_view(), name='list_book'),
    re_path(r'^book/(?P<pk>\d+)/$', views.BookDetailView.as_view(), name='book_detail'),
    re_path(r'^authors/$', views.AuthorListView.as_view(), name='authors_list'),
    re_path(r'^author/(?P<pk>\d+)/$', views.AuthorDetailView.as_view(), name='author_detail'),
]
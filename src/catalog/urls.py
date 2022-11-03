import re
from django.urls import re_path, include, path
# import uuid
from . import views

app_name = 'catalog'

urlpatterns = [
    # re_path(r'^$', views.demo, name='demo'),
    re_path(r'^$', views.index, name="index"),

    re_path(
        r'^book/',
        include(
            [
                re_path(
                    r'^list/$',
                     views.BookListView.as_view(),
                     name='book_list'
                ),
                re_path(
                    r'^add/$',
                    views.AddBookView.as_view(),
                    name='add_book'
                ),
                re_path(
                    r'^(?P<pk>\d+)/detail/$',
                    views.BookDetailView.as_view(),
                    name="book_detail"
                ),
                re_path(
                    r'^(?P<pk>\d+)/delete/$',
                    views.DeleteBookView.as_view(),
                    name='delete_book'
                ),
                re_path(
                    r"^(?P<pk>\d+)/update/$",
                    views.UpdateBookView.as_view(),
                    name='update_book'
                ),
                re_path(
                    r'^loan_book/$',
                    views.LoanedBooksByUserListView.as_view(),
                    name="loaned_book"
                ),
                re_path(
                    r'^loan/',
                    include(
                        [
                            path(
                                "<uuid:pk>/renew",
                                views.RenewDateBookView,
                                name="renew_due_back"
                            ),
                            re_path(
                                r'^list/$',
                                views.ListLoanedBookView.as_view(),
                                name='list_loan'
                            ),
                            # TODO: using class based
                            # path(
                            #     "<uuid:id>/renew/",
                            #     views.RenewDueDateView.as_view(),
                            #     name='renew_ss'
                            # ),
                        ]
                    )
                ),
                re_path(
                    r'^language/',
                    include(
                        [
                            re_path(
                                r'^$',
                                views.ListLanguageView.as_view(),
                                name='list_language'
                            ),
                            re_path(
                                r'^add/$',
                                views.AddLanguageView.as_view(),
                                name='add_language'
                            ),
                        ]
                    )
                ),
            ],
        ),
    ),
]
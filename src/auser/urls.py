from django.urls import re_path, include, reverse_lazy, path

from django.contrib.auth.views import ( LoginView, LogoutView,
                                        PasswordResetView, PasswordChangeDoneView,
                                        PasswordChangeView, PasswordResetCompleteView,
                                        PasswordResetConfirmView, PasswordResetDoneView
                                        )
from auser import views

app_name = "auser"

urlpatterns = [
    re_path(
        r'^auth/',
        include(
            [
                re_path(
                    r"^login/$",
                    LoginView.as_view(
                        redirect_authenticated_user=False,
                        extra_context = {"title": "Login"}
                    ),
                    name="login"
                ),
                re_path(
                    r"^logout/$",
                    LogoutView.as_view(
                        extra_context = {"title": "Log out"}
                    ),
                    name= "logout"
                ),
                re_path(
                    r"^password_rest/$",
                  PasswordResetView.as_view(
                    success_url = reverse_lazy("auser:password_reset_done"),
                    extra_context = {"title": "Password reset"}
                  ),
                  name="password_reset"  
                ),
                path(
                    "reset/<uidb64>/<token>/",
                    PasswordResetConfirmView.as_view(
                        success_url=reverse_lazy("auser:password_reset_complete"),
                        extra_context={"title": "Reset Password"},
                    ),
                    name='password_reset_confirm'
                ),
                re_path(
                    r"^password_change/$",
                    PasswordChangeView.as_view(
                        success_url=reverse_lazy("auser:password_change_done"),
                        extra_context={"title": "Change Password"},
                    ),
                    name="password_change",
                ),
                re_path(r'', include("django.contrib.auth.urls")),
            ],
        )
    ),

    re_path(r'^authors/$', views.AuthorListView.as_view(), name='authors_list'),
    re_path(r'^author/(?P<pk>\d+)/$', views.AuthorDetailView.as_view(), name='author_detail'),
]
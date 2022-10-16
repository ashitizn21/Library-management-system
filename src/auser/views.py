from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.utils.translation import gettext_lazy as _ 
from django.contrib.auth.models import Group

from .models import Author, User
from .forms import UserCreateForm, UpdateRoleForm
class AuthorListView(ListView):

    model = Author
    template_name = "auser/authors_list.html"
    context_object_name = "authors"
    extra_context = {"title": "Authors list"}
        
class AuthorDetailView(DetailView):

    model = Author
    template_name = 'auser/author_detail.html'
    extra_context = {"title": "Author detail"}

class AddUserView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    '''  '''
    model = User
    form_class = UserCreateForm
    template_name = "auser/add_user.html"
    success_message = "Account succesfully created!"
    permission_required = "auser:add_user"
    success_url = reverse_lazy("catalog:index")
    extra_context = {"title": _("Add user")}


class ListUsersView(PermissionRequiredMixin, ListView):
    ''' List users of the system '''
    model = User
    template_name = "auser/list_users.html"
    permission_required = "auser:view_user"
    extra_context = {"title": _("List of users ")}
    context_object_name = "users"


class UpdateUserProfileView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    ''' Update user profile '''
    model = User
    fields = (
        "username",
        "first_name",
        "last_name",
        "email",
        "phone_number",
        "location",
        "po_box",
        "profile_picture",
    )
    template_name = "auser/user/update.html"
    permission_required = "auser.change_user"
    success_url = reverse_lazy("auser:list_user")


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"title": _(f'Update {self.object.get_full_name() }')})
        return context

class ListRolesView(PermissionRequiredMixin, ListView):
    ''' List roles of users '''

    model = Group
    template_name = "auser/role/list.html"
    permission_required = ("auth.view_group",)
    context_objects_name = "roles"
    extra_context = {"title": _("Role list")}

    def get_queryset(self):
        return super().get_queryset().values("pk", "name")

class UpdateRoleView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    ''' Update role of user view '''

    model = Group
    form_class = UpdateRoleForm
    template_name = "auser/role/update.html"
    permission_required = ("auth.change_group")
    success_url = reverse_lazy("auser:list_role")
    success_message = _("Role permissions are updated successfully.")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"title": "update %s permissions" % self.object.name })
        return context

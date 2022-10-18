from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.utils.translation import gettext_lazy as _ 
from django.contrib.auth.models import Group
from django.contrib import messages
from django.db.models import ProtectedError
from django.http import HttpResponseRedirect 

from .models import Author, User
from .forms import UserCreateForm, UpdateRoleForm, UpdateUserForm, AddAuthorForm
class AuthorListView(ListView):

    model = Author
    template_name = "auser/author/list.html"
    context_object_name = "authors"
    extra_context = {"title": "Authors list"}
        
class AddAuthorView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Author
    form_class = AddAuthorForm
    permission_required = "auser.add_author"
    template_name = "auser/author/add.html"
    success_url = reverse_lazy("auser:authors_list")
    extra_context = {"title": _("Add author")}

class AuthorDetailView(DetailView):

    model = Author
    template_name = 'auser/author/detail.html'
    extra_context = {"title": "Author detail"}
    context_object_name = "author"

class AddUserView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    '''  '''
    model = User
    form_class = UserCreateForm
    template_name = "auser/user/add.html"
    success_message = "Account succesfully created!"
    permission_required = "auser:add_user"
    success_url = reverse_lazy("catalog:index")
    extra_context = {"title": _("Add user")}

    # def form_valid(self, form):
    #     if self.is_firstName_required(form):
    #         # print("@@@@pass@@@")
    #         return super().form_valid(form)
    #     # print("@@@@ not @@@")
    #     return super().form_invalid(form)

    # def is_firstName_required(self, form):
    #     firstName = form.cleaned_data['first_name']
    #     if len(firstName) == 0:
    #         print("---null---")
    #         form.add_error(
    #             "first_name",
    #             "Name of author is required, at least enter first name"
    #         )
    #         return False
    #     # print("++++ not null +++")
    #     return True
        

class ListUsersView(PermissionRequiredMixin, ListView):
    ''' List users of the system '''
    model = User
    template_name = "auser/user/list.html"
    permission_required = "auser:view_user"
    extra_context = {"title": _("List of users ")}
    context_object_name = "users"


class UpdateUserProfileView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    ''' Update user profile '''
    model = User
    form_class = UpdateUserForm
    template_name = "auser/user/update.html"
    permission_required = "auser.change_user"
    success_url = reverse_lazy("auser:list_user")

    def get_initial(self):
        initial = super().get_initial()
        try:
            current_group = self.object.groups.get()
        except:
            pass
        else:
            initial['group']=current_group.pk
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"title": _(f'Update {self.object.get_full_name() }')})
        return context

    def form_valid(self, form):
        self.object.groups.clear()
        for nn in form.cleaned_data['group']:
            self.object.groups.add(Group.objects.get(name=nn))
        return super().form_valid(form)

class UserDetailView(PermissionRequiredMixin, DetailView):
    model = User
    permission_required = "auser.view_user"
    template_name = "auser/user/detail.html"
    extra_context = {"title": _("User detail")} 


class DeleteUserView(PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = User
    permission_required = "auser.delete_user"
    success_url = reverse_lazy("auser:list_user")
    http_method_name = ['post']

    def delete(self, request, *args, **kwargs):
        try:
            response = super().delete(request, *args, **kwargs)
            messages.success(
                request,
                f"User {self.object.get_full_name()} deleted successfully.",
            )
            return response
        except ProtectedError as error:
            messages.error(
                request,
                f"You cann't delete this user, because there is {len(error.protected_objects)} "
                "related datas. try to delete related objects first.",
            )
            return HttpResponseRedirect(self.success_url)

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

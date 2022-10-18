import datetime
from pyexpat import model
from django import forms
from django.contrib.auth.models import Group, Permission
from django.core.exceptions import ValidationError
from auser.models import User, Author

class UserCreateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "phone_number",
            "location",
        )

class UpdateRoleForm(forms.ModelForm):
    ''' Form used to update permission of a group user '''
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.select_related("content_type"), required=False
    )

    class Meta:
        model = Group
        fields = ("permissions", )

class UpdateUserForm(forms.ModelForm):
    group = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(), required=True
    )

    class Meta:
        model = User
        fields = (
        "username",
        "first_name",
        "last_name",
        "email",
        "group",
        "phone_number",
        "location",
        "po_box",
        "profile_picture",
    )

class DateInput(forms.DateInput):
    input_type  = 'date'

class AddAuthorForm(forms.ModelForm):

    class Meta:
        model = Author
        fields = ['username', "first_name", "last_name", "email", "phone_number", "sex", "date_of_birth", "date_of_death", "profile_picture"]
        widgets = {
            "date_of_birth": DateInput(),
            "date_of_death": DateInput(),
        }
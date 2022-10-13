
from dataclasses import field
from pyexpat import model
from django import forms
from django.contrib.auth.models import Group, Permission

from auser.models import User

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
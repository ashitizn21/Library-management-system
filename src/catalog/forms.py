import datetime
from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from .models import Book, BookInstance

class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text=_("Enter a date between now and 4 weeks to future, default is 3 weeks."))
    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        # check if its entered date in past or not and as well to the future which more than 4 weeks or not
        if data < datetime.date.today():
            raise ValidationError("Invalid input, entered value is in past")

        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_("Invalid input, entered value is more than 4 weeks ahead"))
        
        return data
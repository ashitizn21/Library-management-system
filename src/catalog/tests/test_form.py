'''
     Test form of auser app
'''
import datetime
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from catalog.forms import RenewBookForm

class TestBookRenewForm(TestCase):
    
    def test_renew_date_field_label(self):
        form = RenewBookForm()
        value = form.fields['renewal_date'].label
        self.assertTrue(value is None or value == "renewal date" )
        
    def test_renewal_date_help_text(self):
        form = RenewBookForm()
        value = form.fields['renewal_date'].help_text
        target = "Enter a date between now and 4 weeks to future, default is 3 weeks."
        self.assertEqual(value, target)

    def test_forms_data(self):
        form_data  = {"renewal_date": "2022-13-03"}
        form = RenewBookForm(data=form_data)
        # print(form)
        self.assertFalse(form.is_valid())

    def test_renewal_date_in_past(self):
        past_date_data  = datetime.date.today() - datetime.timedelta(days=5)
        form = RenewBookForm(data={"renewal_date": past_date_data})
        self.assertTrue(form.is_valid())

    def tes_renewal_date_in_future(self):
        ''' the entered date more than 4 weeeks and if run it correctly, there is a problem '''
        value = datetime.date.today() + datetime.timedelta(weeks=4) + datetime.timedelta(days=1)
        form = RenewBookForm(data={"renewal_date": value})
        self.assertTrue(form.is_valid())

    def tes_renewal_date_in_future_lt_4week(self):
        ''' the entered date less than 4 weeeks and if run it correctly, it is work good'''
        value = datetime.date.today() + datetime.timedelta(weeks=3) + datetime.timedelta(days=1)
        form = RenewBookForm(data={"renewal_date": value})
        self.assertTrue(form.is_valid())
    
    def test_renewal_date_form_date_today(self):
        '''  '''
        value = datetime.date.today()
        form = RenewBookForm(data={"renewal_date": value})
        self.assertTrue(form.is_valid())

    def test_renewal_date_form_date_max(self):
        '''  '''
        value = timezone.localtime() + datetime.timedelta(weeks=4)
        form = RenewBookForm(data={"renewal_date": value})
        self.assertTrue(form.is_valid())

    # def test_renewal_date_raised_error_msg(self):

    #     value = datetime.date.today() + datetime.timedelta(weeks=3) + datetime.timedelta(days=1)
    #     form = RenewBookForm(data={"renewal_date": value})
    #     try:
    #         print("%^^^^^")
    #         form.cleaned_data['renewal_date']
    #         print('[][][]')
    #     except ValidationError as e:
    #         for kk in e.item:
    #             print(kk)

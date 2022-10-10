
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

class PhoneNumberValidator(RegexValidator):
    ''' Phone number validator, used to validate both local and international
        phone number formats, and also accept 3 digit service numbers.

        Attributes:
        regex: regeular expression that represent phone number replace super class default empty value.
        message: message to be displayed if validation fail.
        code: code name used to identify error when raises.
     '''
    FORMAT = r"^((\+251|09)\d{8} | (\+251\d{6}))$"
    message = _("Please enter your phone number in +2519********" " or 09******** format.")
    error_code = "invalid_phone_number"
    
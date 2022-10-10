from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from auser.validators import PhoneNumberValidator

class Address(models.Model):
    """
    An abstract class which represent composite attribute 'Address'
    for sub classes.
    """

    phone_number = models.CharField(
        _("phone number"),
        max_length=13,
        unique=True,
        help_text=_("Use the format +2519********" " or 09********."),
        validators=[PhoneNumberValidator()],
    )
    location = models.CharField(
        _("address"),
        max_length=200,
        blank=True,
        null=True,
        help_text=_("Physical location."),
    )
    po_box = models.CharField(
        _("P.O Box"), max_length=10, blank=True, null=True, help_text=_("Personal P.O Box, if you have one.")
    )

    class Meta:
        abstract = True

class User(AbstractUser, Address):
    '''  '''
    class SexChoices(models.TextChoices):
        MALE = "M", _("MALE")
        FEMALE = "F", _("FEMALE")

    
    email = models.EmailField(
        _("email address"),
        unique=True,
        help_text=_("Active email you use.")
    )
    sex = models.CharField(_("gender"), max_length=2, choices=SexChoices.choices, null=True)
    profile_picture = models.ImageField(_("profile picture"), upload_to="profile_pictures/", default="default.svg")

    class Meta:
        db_table = "user"
        verbose_name = "User"
        verbose_name_plural = "Users"
        
    def __str__(self):
        ff = f"{self.username} {('--'+self.get_full_name()) if self.get_full_name() else ' '}"
        return ff


class Author(User):
    ''' Author model of books '''
   
    date_of_birth = models.DateField(_("date of birth"), null=True, blank=True)
    date_of_death = models.DateField(_("Died"), null=True, blank=True)

    class Meta:
        ordering = ["last_name", "first_name"]
        db_table = "author"
        verbose_name = _("author")
        verbose_name_plural = _("authors")

    def get_absolute_url(self):
        return reverse('catalog:author_detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'

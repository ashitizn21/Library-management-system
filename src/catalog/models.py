from random import choices
from secrets import choice
from tkinter import CASCADE
from django.db import models
from django.utils.translation import gettext_lazy as _

class Author(models.Model):
    ''' Author model of books '''
    name = models.CharField(_("name"), max_length=100)
    date_of_birth = models.DateField(_("date of birth"))
    date_of_death = models.DateField(_("date of death"))

    class Meta:
        ordering = ["name"]
        db_table = "author"
        verbose_name = _("author")
        verbose_name_plural = _("authors")


class Book(models.Model):
    ''' books '''
    class GenreChoices(models.IntegerChoices):
        Science_Fiction = 0, _("Science fiction")
        Fantacy = 1, _("fantacy")
        Western = 2, _("western")
        French_Poetry = 3, _("french poetry")
        
    title = models.CharField(_("title"), max_length=200)
    author = models.ForeignKey(
            Author,
            related_name = 'books',
            on_delete=models.CASCADE
            )
    genre = models.SmallIntegerField(
        _("genre"),
        choices=GenreChoices.choices,
        default=GenreChoices.Science_Fiction,
        help_text = _("select genre of book. by default Science fiction genre selected")
    )    
    
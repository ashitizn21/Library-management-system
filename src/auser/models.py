from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

class Author(models.Model):
    ''' Author model of books '''
    first_name = models.CharField(_("first name"), max_length=100)
    last_name  = models.CharField(_("last name"), max_length=100)
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

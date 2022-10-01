
from secrets import choice
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
import uuid 

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
        return reverse('author_detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'


class Genre(models.Model):
    ''' genres of books '''
    name = models.CharField(max_length=200, help_text=_("Enter a book genre"))

    def __str__(self):
        return self.name


class Book(models.Model):
    ''' books '''
            
    title = models.CharField(_("title"), max_length=200)
    author = models.ForeignKey(
            Author,
            related_name = 'books',
            on_delete=models.SET_NULL,
            null=True
            )
    genre = models.ManyToManyField(Genre, help_text="select a genre of this book")
    summary = models.TextField(max_length=1000, help_text=_("Enter a brief description of the book"))
    isbn = models.CharField('ISBN', max_length=13, unique=True,
                             help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')

    class Meta:
        ordering = ['title']
        db_table = "book"
        verbose_name = _("book")
        verbose_name_plural = _("books") 

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'
class BookInstance(models.Model):
    ''' copies of book '''

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, 
                          help_text=_("Unique ID for this particular book across whole library"))
    book = models.ForeignKey(Book, on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('M', "Maintenance"),
        ('O', "On loan"),
        ('A', "Available"),
        ('R', "Reserved"),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS,
                             blank=True,
                             default='M',
                             help_text=_("book availability"),)

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        return f'{self.id} ({self.book.title})'
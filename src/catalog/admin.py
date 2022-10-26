from django.contrib import admin

from .models import Genre, Book, BookInstance
from auser.models import Author

class AuthorBookInline(admin.TabularInline):
    '''  '''
    model = Book
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ["username", "first_name", "last_name", "date_of_birth", "date_of_death"]
    fields = ['first_name', "last_name", "username", "email", "phone_number", ("date_of_birth", "date_of_death")]

    inlines = [AuthorBookInline]
class BookInstanceInline(admin.TabularInline):
    ''' to see instance of book in detail of book '''
    model = BookInstance

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    
    inlines = [BookInstanceInline]

class BookInstanceAdmin(admin.ModelAdmin):
    list_filter = ('status', 'due_back')
    list_display = ('book', 'status', 'due_back')

    fieldsets = (
        (None, {
            "fields": ("id", "book", "imprint")
        }),
        ('Availability', {
            "fields": ("status", "due_back", "borrower")
        }),
    )
admin.site.register(BookInstance, BookInstanceAdmin)

class GenreAdmin(admin.ModelAdmin):
    pass

admin.site.register(Genre, GenreAdmin)
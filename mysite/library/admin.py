from django.contrib import admin

# Register your models here.
from .models import Author, Genre, Book, BookInstance, BookReview, Profilis

class AuthorAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name", "display_books")

class BooksInstanceInline(admin.TabularInline):
    model = BookInstance
    # readonly_fields = ("id",)
    # can_delete = False
    extra = 0

class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "display_genre")
    inlines = [BooksInstanceInline]

class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ("book", "status", "reader", "due_back")
    list_editable = ("due_back", "status")
    list_filter = ("status", "due_back")
    search_fields = ("id", "book__title")
    fieldsets = (
        ("General", {"fields": ("id", "book")}),
        ("Availability", {"fields": ("status", "due_back", "reader")})
    )

class BookReviewAdmin(admin.ModelAdmin):
    list_display = ("book", "date_created", "reviewer", "content")

admin.site.register(Book, BookAdmin)
admin.site.register(Genre)
admin.site.register(Author, AuthorAdmin)
admin.site.register(BookInstance, BookInstanceAdmin)
admin.site.register(BookReview, BookReviewAdmin)
admin.site.register(Profilis)


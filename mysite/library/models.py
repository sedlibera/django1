from django.db import models
from django.urls import reverse
import uuid

class Genre(models.Model):
    name = models.CharField("Pavadinimas",
                            max_length=200,
                            help_text="Iveskite knygos žanrą(pvz. detektyvas)")

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField("Pavadinimas", max_length=200)
    author = models.ForeignKey("Author", on_delete=models.SET_NULL, null=True)
    summary = models.TextField("Aprasymas", max_length=1000, help_text="Trumpas knygos aprašymas")
    isbn = models.CharField("ISBN", max_length=13)
    genre = models.ManyToManyField(Genre, help_text="Išrinkite žantą(us) šiai knygai")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("book-detail", args=[str(self.id)])

class Author(models.Model):
    first_name = models.CharField("Vardas", max_length=100)
    last_name = models.CharField("Pavarde", max_length=100)

    class Meta:
        ordering = ["last_name", "first_name"]

    def get_absolute_url(self):
        return reverse("author-detail", args=[str(self.id)])

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unikalus ID knygos kopijai")
    book = models.ForeignKey("Book", on_delete=models.SET_NULL, null=True)
    due_back = models.DateField("Bus prieinama", null=True, blank=True)

    LOAN_STATUS = (
        ("a", "Administruojama"),
        ("p", "Paimta"),
        ("g", "Galima paimti"),
        ("r", "Rezervuota")
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default="a", help_text="Statusas")

    class Meta:
        ordering = ["due_back"]

    def __str__(self):
        return f"{self.id} ({self.book.title})"


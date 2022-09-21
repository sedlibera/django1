from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Book, Author, BookInstance, Genre
from django.views import generic

def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status="g").count()
    # num_instances_available = BookInstance.objects.filter(status__exact="g").count()
    num_authors = Author.objects.count()

    kontext = {"num_books": num_books, "num_instances": num_instances,
               "num_instances_available": num_instances_available,
               "num_authors": num_authors}

    return render(request, "index.html", context=kontext)

def authors(request):

    autoriai = Author.objects.all()
    kontext = {
        "authors": autoriai
    }
    return render(request, "authors.html", context=kontext)

def author(request, author_id):
    single_author = get_object_or_404(Author, pk=author_id)
    return render(request, "author.html", {"author": single_author})

class BookListView(generic.ListView):
    model = Book
    template_name = "book_list.html"

class BookDetailView(generic.DetailView):
    model = Book
    template_name = "book_detail.html"


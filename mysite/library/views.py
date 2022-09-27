import logging

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Book, Author, BookInstance, Genre
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q

def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status="g").count()
    # num_instances_available = BookInstance.objects.filter(status__exact="g").count()
    num_authors = Author.objects.count()

    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    kontext = {"num_books": num_books, "num_instances": num_instances,
               "num_instances_available": num_instances_available,
               "num_authors": num_authors,
               "num_visits": num_visits}

    return render(request, "index.html", context=kontext)

def authors(request):
    paginator = Paginator(Author.objects.all(), 2)
    page_number = request.GET.get('page')
    paged_authors = paginator.get_page(page_number)
    kontext = {"authors": paged_authors}
    return render(request, "authors.html", context=kontext)

def author(request, author_id):
    single_author = get_object_or_404(Author, pk=author_id)
    return render(request, "author.html", {"author": single_author})

def search(request):
    query_text = request.GET.get("query")
    # search_results = Book.objects.filter(title__icontains=query_text)
    search_results = Book.objects.filter(
                                        Q(title__icontains=query_text) | Q(summary__icontains=query_text))
    return render(request, "search.html", {"books": search_results, "querytxt": query_text})

class BookListView(generic.ListView):
    model = Book
    paginate_by = 2
    template_name = "book_list.html"

class BookDetailView(generic.DetailView):
    model = Book
    template_name = "book_detail.html"


import logging

from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponse
from .models import Book, Author, BookInstance, Genre
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from .forms import BookReviewForm, UserUpdateForm, ProfilisUpdateForm
from django.views.generic.edit import FormMixin
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _


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

class BookDetailView(FormMixin, generic.DetailView):
    model = Book
    template_name = "book_detail.html"
    form_class = BookReviewForm

    class Meta:
        ordering = ["title"]

    def get_success_url(self):
        return reverse("book-detail", kwargs={"pk": self.object.id})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.book = self.object
        form.instance.reviewer = self.request.user
        form.save()
        return super(BookDetailView, self).form_valid(form)





class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance  # konteksto kintamasis i sablona bookinstance_list
    template_name = "user_books.html"
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(reader=self.request.user).filter(status__exact="p").order_by("due_back")

@csrf_protect
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        laukai = [username, email, password, password2]
        if not all(laukai):
            messages.error(request, _(f"All fields bust be filled!"))
            return redirect("register")
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, _("Username %s already exists!") % username)
                return redirect("register")
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, _("Email %s already exists!") % email)
                    return redirect("register")
                else:
                    User.objects.create_user(username, email=email, password=password)
                    messages.success(request, _("User %s created") % username)
        else:
            messages.error(request, _("Passwords do not match!!!"))
            return redirect("register")
    return render(request, "register.html")

# @login_required
# def profilis(request):
#     return render(request, "profilis.html")

@login_required
def profilis(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfilisUpdateForm(request.POST, request.FILES, instance=request.user.profilis)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Profilis atnaujintas")
            return redirect("profilis")
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfilisUpdateForm(instance=request.user.profilis)

    context = {"u_form": u_form, "p_form": p_form}

    return render(request, "profilis.html", context)

class BookByUserDetailView(LoginRequiredMixin, generic.DetailView):
    model = BookInstance
    template_name = "user_book.html"

class BookByUserCreateView(LoginRequiredMixin, generic.CreateView):
    model=BookInstance
    fields = ["book", "due_back"]
    success_url = "/library/mybooks/"
    template_name = "user_book_form.html"

    def form_valid(self, form):
        form.instance.reader = self.request.user
        return super().form_valid(form)

class BookByUserUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = BookInstance
    fields = ["book", "due_back"]
    success_url = "/library/mybooks/"
    template_name = "user_book_form.html"

    def form_valid(self, form):
        form.instance.reader = self.request.user
        return super().form_valid(form)

    def test_func(self):
        book = self.get_object()
        return self.request.user == book.reader

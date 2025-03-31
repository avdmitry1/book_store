from django.shortcuts import redirect, render
from django.views.generic import ListView

from books.models import Book
from rentals.models import Rental

from .forms import SearchBookForm


def search_book_view(request):
    form = SearchBookForm(request.POST or None)

    if form.is_valid():
        search_query = form.cleaned_data["search"]
        book = Book.objects.filter(isbn=search_query).first()
        if book:
            return redirect("rentals:detail", book_id=book.isbn)

    context = {"form": form}
    return render(request, "rentals/main.html", context)


class BookRentalHistoryView(ListView):
    model = Rental
    template_name = "rentals/detail.html"

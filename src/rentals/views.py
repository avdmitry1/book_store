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

    def get_queryset(self):
        book_id = self.kwargs.get("book_id")
        return Rental.objects.filter(book__isbn=book_id)

    def get_context_data(self, **kwargs):
        contex = super().get_context_data(**kwargs)
        qs = self.get_queryset()
        obj = None
        if qs.exists():
            obj = qs.first()
        contex["object"] = obj
        return contex

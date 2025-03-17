from django.db.models import QuerySet
from django.http import HttpRequest
from django.shortcuts import HttpResponse, get_object_or_404, render
from django.views.generic import FormView, ListView

from .forms import BookTitleForm
from .models import BookTitle


class BookTitleListView(FormView, ListView):
    """
    Displays a list of BookTitles and handles form submission to create new ones.
    """

    queryset = BookTitle.objects.all()
    template_name = "books/main.html"
    context_object_name = "object_list"
    form_class = BookTitleForm

    def get_success_url(self) -> str:
        """Returns the redirect URL after a successful form submission."""
        return self.request.path

    def form_valid(self, form: BookTitleForm) -> HttpResponse:
        """Saves the form and redirects on success."""
        form.save()
        return super().form_valid(form)

    def get_queryset(self) -> QuerySet[BookTitle]:
        """Returns books with titles containing 'i'."""
        return BookTitle.objects.filter(title__contains="i")


def book_title_detail_view(request: HttpRequest, pk: int) -> HttpResponse:
    """
    Displays a single BookTitle object by its primary key (pk).
    """
    obj = get_object_or_404(BookTitle, id=pk)
    return render(request, "books/detail.html", {"obj": obj})

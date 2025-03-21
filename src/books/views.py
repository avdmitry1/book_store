from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import FormView, ListView

from .forms import BookTitleForm
from .models import BookTitle
from django.contrib import messages
import string


class BookTitleListView(FormView, ListView):
    # queryset: QuerySet[BookTitle] = BookTitle.objects.all()
    template_name: str = "books/main.html"
    context_object_name: str = "object_list"
    form_class: type = BookTitleForm

    def get_success_url(self) -> str:
        return self.request.path

    def form_valid(self, form: BookTitleForm) -> HttpResponse:
        book_title: BookTitle = form.save()
        messages.add_message(self.request, messages.INFO, f"'{book_title}' created.")
        return super().form_valid(form)

    def form_invalid(self, form: BookTitleForm) -> HttpResponse:
        self.object_list = self.get_queryset()
        messages.add_message(self.request, messages.ERROR, form.errors)
        return super().form_invalid(form)

    def get_queryset(self) -> QuerySet[BookTitle]:
        parameter = self.kwargs.get("letter", "a")
        return BookTitle.objects.filter(title__startswith=parameter)

    def get_context_data(self, **kwargs) -> dict:
        """Return the context data for the list view."""
        context = super().get_context_data(**kwargs)
        context["letters"] = list(string.ascii_lowercase)
        context["selected_letter"] = self.kwargs.get("letter", "a")
        return context


def book_title_detail_view(request: HttpRequest, pk: int) -> HttpResponse:
    obj: BookTitle = get_object_or_404(BookTitle, id=pk)
    return render(request, "books/detail.html", {"obj": obj})

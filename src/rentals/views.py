from datetime import datetime, timezone

from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import CreateView, FormView, ListView, UpdateView

from books.models import Book
from rentals.models import Rental

from .admin import RentalResource
from .choices import FORMAT_CHOICES
from .forms import SearchBookForm, SelectExportOptionForm


def search_book_view(request):
    form = SearchBookForm(request.POST or None)

    if form.is_valid():
        search_query = form.cleaned_data["search"]
        book = Book.objects.filter(Q(isbn=search_query) | Q(id=search_query)).exists()
        if book:
            return redirect("rentals:detail", search_query)

    context = {"form": form}
    return render(request, "rentals/main.html", context)


class BookRentalHistoryView(ListView):
    model = Rental
    template_name = "rentals/detail.html"

    def get_queryset(self):
        book_id = self.kwargs.get("book_id")
        return Rental.objects.filter(Q(book__isbn=book_id) | Q(book__id=book_id))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book_id = self.kwargs.get("book_id")
        obj = Book.objects.filter(Q(isbn=book_id) | Q(id=book_id)).first()
        # obj = get_object_or_404(Book, Q(isbn=book_id) | Q(id=book_id))
        context["object"] = obj
        context["book_id"] = book_id
        return context


class UpdateRentalStatusView(UpdateView):
    model = Rental
    template_name = "rentals/update.html"
    fields = ("status",)

    def get_success_url(self):
        book_id = self.kwargs.get("book_id")
        return reverse("rentals:detail", kwargs={"book_id": book_id})

    def form_valid(self, form):
        instance = form.save(commit=False)
        if instance.status == 1:
            instance.return_date = timezone.now()
        instance.is_closed = True
        instance.save()
        messages.add_message(self.request, messages.INFO, "Rental status updated.")
        return super().form_valid(form)


class CreateNewRentalView(CreateView):
    model = Rental
    template_name = "rentals/new.html"
    fields = ("customer",)

    def get_success_url(self):
        book_id = self.kwargs.get("book_id")
        return reverse("rentals:detail", kwargs={"book_id": book_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["book_id"] = self.kwargs.get("book_id")
        return context

    def form_valid(self, form):
        instance = form.save(commit=False)
        book_id = self.kwargs.get("book_id")
        obj = Book.objects.get(id=book_id)
        instance.book = obj
        instance.status = 0
        instance.rent_start_date = datetime.today().date()
        instance.save()
        return super().form_valid(form)


class SelectDownloadRentalsView(FormView):
    template_name = "rentals/select_format.html"
    form_class = SelectExportOptionForm

    def get_success_url(self):
        return self.request.path

    def get_context_data(self, **kwargs):
        # Викликаємо метод get_context_data з батьківського класу
        context = super().get_context_data(**kwargs)
        book_id = self.kwargs.get("book_id")
        context["book_id"] = book_id
        return context

    def post(self, request, **kwargs):
        # pip install django-import-export tablib openpyxl xlwt xlrd
        try:
            selected_format = request.POST.get("format")

            # Перевіряємо, чи вибрано дійсний формат
            if selected_format not in ["csv", "xls", "json"]:
                messages.error(request, f"Invalid format selected: {selected_format}")
                return redirect(self.get_success_url())

            # Отримуємо ID книги
            book_id = self.kwargs.get("book_id")
            if not book_id:
                messages.error(request, "Book ID is missing.")
                return redirect(self.get_success_url())

            # Отримуємо всі записи для книги
            rentals = Rental.objects.filter(Q(book__isbn=book_id) | Q(book__id=book_id))
            if not rentals.exists():
                messages.error(request, "No rentals found for this book.")
                return redirect(self.get_success_url())

            # Створюємо ресурс і єкспортуємо данні
            resource = RentalResource()
            dataset = resource.export(rentals)

            # Налаштовуємо тип контенту для скачування
            content_types = {
                "csv": "text/csv",
                "xls": "application/vnd.ms-excel",
                "json": "application/json",
            }

            # Єкспортуємо данні за допомогою вибраного формату
            if selected_format == "csv":
                data = dataset.export("csv")
            elif selected_format == "xls":
                data = dataset.export("xls")
            elif selected_format == "json":
                data = dataset.export("json")

            # Формуємо відповідь для скачування
            response = HttpResponse(data, content_type=content_types[selected_format])
            response["Content-Disposition"] = (
                f'attachment; filename="{book_id}.{selected_format}"'
            )
            return response

        except Exception as error:
            import traceback

            traceback.print_exc()  # Виводить детальну інформацію про виняток
            messages.error(request, f"An error occurred during export: {error}")
            return redirect(self.get_success_url())

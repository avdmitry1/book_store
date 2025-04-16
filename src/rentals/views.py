from datetime import datetime, timezone

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import CreateView, FormView, ListView, UpdateView

from books.models import Book
from rentals.models import Rental

from .admin import RentalResource
from .forms import SearchBookForm, SelectExportOptionForm


@login_required
def search_book_view(request):
    # Ініціалізуємо форму пошуку з даними POST або None (якщо GET-запит)
    form = SearchBookForm(request.POST or None)
    if form.is_valid():  # Перевіряємо, чи форма валідна
        # Отримуємо пошуковий запит з очищених даних форми
        search_query = form.cleaned_data["search"]
        # Перевіряємо, чи існує книга з таким ISBN або ID
        # Використовуємо Q-об'єкти для пошуку за двома полями
        book = Book.objects.filter(Q(isbn=search_query) | Q(id=search_query)).exists()
        if book:  # Якщо книга знайдена
            # Перенаправляємо на сторінку деталей книги, передаючи search_query як параметр
            return redirect("rentals:detail", search_query)
    # Готуємо контекст для шаблону (в даному випадку - лише форму)
    context = {"form": form}
    # Рендеримо шаблон "rentals/main.html" з переданим контекстом
    return render(request, "rentals/main.html", context)


class BookRentalHistoryView(LoginRequiredMixin, ListView):
    # Представлення для відображення історії оренди книги
    model = Rental  # Вказуємо модель, з якою працює це представлення (модель Rental)
    template_name = "rentals/detail.html"  # Шлях до шаблону, який використовуватиметься для відображення

    def get_queryset(self):
        # Метод для отримання набору даних (queryset), який буде відображатись у шаблоні
        book_id = self.kwargs.get("book_id")  # Отримуємо book_id з URL-параметрів
        # Фільтруємо записи Rental за ISBN або ID книги
        return Rental.objects.filter(Q(book__isbn=book_id) | Q(book__id=book_id))
        # Використовуємо Q-об'єкти для OR умови (або ISBN, або ID)

    def get_context_data(self, **kwargs):
        # Метод для додавання додаткового контексту до шаблону
        context = super().get_context_data(**kwargs)  # Отримуємо базовий контекст
        book_id = self.kwargs.get("book_id")  # Знову отримуємо book_id

        # Знаходимо книгу за ISBN або ID (беремо перший результат)
        obj = Book.objects.filter(Q(isbn=book_id) | Q(id=book_id)).first()
        # Альтернативний варіант (закоментований) - викликає 404, якщо книга не знайдена
        # obj = get_object_or_404(Book, Q(isbn=book_id) | Q(id=book_id))

        context["object"] = obj  # Додаємо книгу до контексту під ключем "object"
        context["book_id"] = book_id  # Додаємо book_id до контексту
        return context  # Повертаємо оновлений контекст


class UpdateRentalStatusView(LoginRequiredMixin, UpdateView):
    # Представлення для оновлення статусу оренди
    model = Rental  # Вказуємо модель, з якою працює це представлення (модель Rental)
    template_name = "rentals/update.html"  # Шлях до шаблону для сторінки оновлення
    fields = ("status",)  # Вказуємо, що тільки поле 'status' можна редагувати

    def get_success_url(self):
        # Метод визначає URL для перенаправлення після успішного оновлення
        book_id = self.kwargs.get("book_id")  # Отримуємо ID книги з URL-параметрів
        # Генеруємо URL для сторінки деталей оренди цієї книги
        return reverse("rentals:detail", kwargs={"book_id": book_id})

    def form_valid(self, form):
        # Метод викликається при успішній валідації форми
        instance = form.save(
            commit=False
        )  # Отримуємо об'єкт Rental, але не зберігаємо в БД
        # Якщо статус змінений на 1 (наприклад, "Повернено")
        if instance.status == 1:
            instance.return_date = (
                timezone.now()
            )  # Встановлюємо поточну дату як дату повернення
        instance.is_closed = True  # Позначаємо оренду як закриту
        instance.save()  # Зберігаємо зміни в базі даних
        # Додаємо повідомлення про успішне оновлення статусу
        messages.add_message(self.request, messages.INFO, "Rental status updated.")
        # Викликаємо батьківський метод для стандартної обробки
        return super().form_valid(form)


class CreateNewRentalView(LoginRequiredMixin, CreateView):
    # Представлення для створення нової оренди
    # Модель, з якою працює CreateView
    model = Rental
    # Шаблон, який використовується для відображення форми
    template_name = "rentals/new.html"
    # Поля форми, які будуть відображатися
    fields = ("customer",)

    def get_success_url(self):
        book_id = self.kwargs.get("book_id")
        return reverse("rentals:detail", kwargs={"book_id": book_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["book_id"] = self.kwargs.get("book_id")
        return context

    def form_valid(self, form):
        # Метод викликається при успішній валідації форми
        # Зберігаємо форму без коміту в БД, щоб додати додаткові дані
        instance = form.save(commit=False)
        # Отримуємо ідентифікатор книги з URL
        book_id = self.kwargs.get("book_id")
        # Знаходимо книгу за ідентифікатором
        obj = Book.objects.get(id=book_id)
        # Встановлюємо додаткові поля оренди
        instance.book = obj  # Прив'язуємо оренду до книги
        instance.status = 0  # Встановлюємо статус (0 - активна оренда)
        instance.rent_start_date = (
            datetime.today().date()
        )  # Поточна дата як дата початку оренди

        # Зберігаємо оренду в БД
        instance.save()

        # Викликаємо метод form_valid батьківського класу для завершення обробки
        return super().form_valid(form)


class SelectDownloadRentalsView(LoginRequiredMixin, FormView):
    # Шаблон, який використовується для відображення форми
    template_name = "rentals/select_format.html"
    # Клас форми, яка буде використовуватися
    form_class = SelectExportOptionForm

    def get_success_url(self):
        return self.request.path

    def get_context_data(self, **kwargs):
        # Викликаємо метод get_context_data з батьківського класу
        context = super().get_context_data(**kwargs)
        # Отримуємо ідентифікатор книги з параметрів URL
        book_id = self.kwargs.get("book_id")
        # Додаємо ідентифікатор книги до контексту
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

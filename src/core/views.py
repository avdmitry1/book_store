from datetime import datetime

import pyotp
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Count
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView

from books.models import Book, BookTitle
from customers.models import Customer
from publishers.models import Publisher
from rentals.choices import STATUS_CHOICES
from rentals.models import Rental

from .forms import LoginForm, OTPForm
from .utils import send_otp


def login_view(request):
    form = LoginForm(request.POST or None)  # Ініціалізуємо форму з POST-даними

    if request.method == "POST":
        if form.is_valid():  # Якщо форма пройшла валідацію
            username = form.cleaned_data.get("username")  # Отримуємо ім’я користувача
            password = form.cleaned_data.get("password")  # Отримуємо пароль
            user = authenticate(
                request, username=username, password=password
            )  # Перевірка автентифікації

            if user is not None:
                send_otp(request)  # Надсилаємо одноразовий код (OTP)
                request.session["username"] = (
                    username  # Зберігаємо ім’я користувача в сесії для подальшої перевірки OTP
                )
                print("ok, sending OTP")  # Лог для розробника
                return redirect("otp")  # Перенаправлення на сторінку з OTP
            else:
                messages.add_message(
                    request, messages.ERROR, "Invalid username or password."
                )  # Повідомлення про помилку

    context = {"form": form}
    return render(request, "login.html", context)


def otp_view(request):
    error_message = None  # Змінна для збереження повідомлення про помилку
    # Ініціалізація форми з POST-даними (або порожньої, якщо GET-запит)
    form = OTPForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():  # Перевірка, чи форма валідна
            otp = form.cleaned_data.get("otp")  # Отримання введеного користувачем OTP
            username = request.session.get("username")  # Ім'я користувача з сесії
            otp_secret_key = request.session.get(
                "otp_secret_key"
            )  # Секретний ключ для генерації OTP
            otp_valid_until = request.session.get(
                "otp_valid_date"
            )  # Час, до якого дійсний OTP

            if otp_secret_key and otp_valid_until:
                # Перетворення ISO-рядка у datetime
                valid_until = datetime.fromisoformat(otp_valid_until)

                if valid_until > datetime.now():  # Перевірка, чи ще дійсний OTP
                    # Генератор OTP з інтервалом 60 сек.
                    totp = pyotp.TOTP(otp_secret_key, interval=60)

                    if totp.verify(otp):  # Перевірка, чи OTP правильний
                        # Отримання користувача з бази
                        user = get_object_or_404(User, username=username)
                        login(request, user)  # Вхід користувача в систему
                        # Видалення даних OTP із сесії після успішного входу
                        del request.session["otp_secret_key"]
                        del request.session["otp_valid_date"]
                        return redirect("home")  # Перенаправлення на головну сторінку
                    else:
                        error_message = (
                            "Невірний одноразовий код"  # Якщо код неправильний
                        )
                else:
                    error_message = "Термін дії коду вичерпано"  # Якщо термін дії минув
            else:
                error_message = (
                    "Код не знайдено в сесії"  # Якщо дані не збережено в сесії
                )

        # Якщо виникла помилка — додаємо її до повідомлень
        if error_message:
            messages.add_message(request, messages.ERROR, error_message)

    context = {"form": form}
    return render(request, "otp.html", context)


def change_theme(request):
    """
    Toggle the theme between light and dark mode.
    This function checks the current theme in the session and toggles it.
    """
    # Check if the theme is not set in the session
    if request.session.get("is_dark_mode") is None:
        # If it's not set, set the theme to dark mode by default
        request.session["is_dark_mode"] = True
    else:
        # Otherwise, toggle the current theme
        request.session["is_dark_mode"] = not request.session["is_dark_mode"]

    # Redirect to the previous page or the homepage if no referer exists
    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))


class DashBoardView(TemplateView):
    template_name = "dashboard.html"


def chart_data(request):
    # books and book titles (bar)
    data = []
    all_books = len(Book.objects.all())
    all_books_title = len(BookTitle.objects.all())
    data.append(
        {
            "labels": ["books", "book titles"],
            "data": [all_books, all_books_title],
            "description": "Unique book titles vs books",
            "type": "bar",
        },
    )

    # book title count by publisher (pie)
    title_by_publisher = BookTitle.objects.values("publisher__name").annotate(
        count=Count("publisher__name")
    )
    publisher_name = [x["publisher__name"] for x in title_by_publisher]
    publisher_name_count = [x["count"] for x in title_by_publisher]
    data.append(
        {
            "labels": publisher_name,
            "data": publisher_name_count,
            "description": "Book title count by publisher",
            "type": "pie",
        }
    )

    # book by status (pie)
    book_by_status = Rental.objects.values("status").annotate(
        count=Count("book__title")
    )
    book_by_title_count = [x["count"] for x in book_by_status]
    status_keys = [x["status"] for x in book_by_status]
    status = [dict(STATUS_CHOICES)[key] for key in status_keys]
    data.append(
        {
            "labels": status,
            "data": book_by_title_count,
            "description": "Book by status",
            "type": "pie",
        }
    )

    # publishers vs customers (bar)
    customers = len(Customer.objects.all())
    publishers = len(Publisher.objects.all())
    data.append(
        {
            "labels": ["publishers", "customers"],
            "data": [publishers, customers],
            "description": "Publishers vs customers",
            "type": "bar",
        }
    )
    return JsonResponse({"data": data})


# def home_view(request):
#     """
#     This view renders the homepage with a list of customers and the first book's details.
#     If no books exist, it handles the absence gracefully.
#     """
#     # Get all customers from the database
#     qs = Customer.objects.all()

#     # Get the first book title object from the BookTitle model
#     obj = BookTitle.objects.first()

#     # If a book exists, get its books and title; otherwise, set to None and a default title
#     books = obj.books if obj else None
#     title = obj.title if obj else "No books available"

#     # Prepare the context to send to the template
#     context = {"qs": qs, "books": books, "title": title}

#     # Render the homepage with the context
#     return render(request, "main.html", context)

from django.db.models import Count
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic import TemplateView

from books.models import Book, BookTitle
from customers.models import Customer
from publishers.models import Publisher
from rentals.models import Rental
from rentals.choices import STATUS_CHOICES


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
    print(status)
    return JsonResponse({"msg": data})


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

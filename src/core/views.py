from django.http import HttpResponseRedirect
from django.shortcuts import render
from books.models import BookTitle
from customers.models import Customer


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


def home_view(request):
    """
    This view renders the homepage with a list of customers and the first book's details.
    If no books exist, it handles the absence gracefully.
    """
    # Get all customers from the database
    qs = Customer.objects.all()

    # Get the first book title object from the BookTitle model
    obj = BookTitle.objects.first()

    # If a book exists, get its books and title; otherwise, set to None and a default title
    books = obj.books if obj else None
    title = obj.title if obj else "No books available"

    # Prepare the context to send to the template
    context = {"qs": qs, "books": books, "title": title}

    # Render the homepage with the context
    return render(request, "main.html", context)

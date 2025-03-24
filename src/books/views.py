import string

from django.contrib import messages
from django.db.models import QuerySet
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import FormView, ListView, DetailView

from .forms import BookTitleForm
from .models import Book, BookTitle


class BookTitleListView(FormView, ListView):
    """
    A view that displays a list of BookTitle objects and allows the user to add a new
    BookTitle object to the list.

    The view uses the BookTitleForm to validate the user's input. If the input is
    valid, it saves the form data to create a new BookTitle object and adds an
    informational message to be displayed to the user indicating that a new
    BookTitle has been successfully created.

    If the input is invalid, it adds an error message for each error to the messages
    framework, prefixes the message with the field name if the error is a field-
    specific error, and calls the parent class's form_invalid method.

    The view also overrides the get_success_url method to return the current URL
    as the success URL.
    """

    queryset: QuerySet[BookTitle] = BookTitle.objects.all()
    template_name: str = "books/main.html"
    context_object_name: str = "object_list"
    form_class: type = BookTitleForm

    def get_success_url(self) -> str:
        return self.request.path

    def form_valid(self, form: BookTitleForm) -> HttpResponse:
        # Save the form data to create a new BookTitle instance
        book_title: BookTitle = form.save()
        # Add an informational message to be displayed to the user indicating
        # that a new BookTitle has been successfully created
        messages.add_message(self.request, messages.INFO, f"{book_title} created.")
        # Call the parent class's form_valid method to complete the process
        # and redirect the user to the success URL
        return super().form_valid(form)

    def form_invalid(self, form: BookTitleForm) -> HttpResponse:
        self.object_list = self.get_queryset()

        # Loop through the form errors. For each error:
        for field_name, field_errors in form.errors.items():
            # If the error is an "__all__" error (i.e. not a field-specific error),
            # loop through the error messages and add a message for each one.
            if field_name == "__all__":
                for error_message in field_errors:
                    messages.add_message(self.request, messages.ERROR, error_message)
            # If the error is a field-specific error, loop through the error messages
            # and add a message for each one, but prefix the message with the field
            # name.
            else:
                for error_message in field_errors:
                    messages.add_message(
                        self.request,
                        messages.ERROR,
                        f"{field_name.capitalize()}: {error_message}",
                    )
        # Call the parent's form_invalid method.
        return super().form_invalid(form)

    def get_queryset(self) -> QuerySet[BookTitle]:
        parameter = self.kwargs.get("letter", "a")
        # The parameter is a single letter, so we filter the BookTitle objects
        # by the first letter of their title.
        return BookTitle.objects.filter(title__startswith=parameter)

    def get_context_data(self, **kwargs) -> dict:
        # Call the parent class's get_context_data method to get the context data.
        # Then add two additional values to the context data: "letters" and
        # "selected_letter".
        #
        # The "letters" value is a list of all the lowercase letters of the
        # alphabet. This is used in the template to render a list of all the
        # letters of the alphabet, and the "selected_letter" value is used to
        # determine which letter to highlight in the list.
        #
        # The "selected_letter" value is the value of the "letter" parameter from
        # the URL pattern (or "a" if no "letter" parameter is provided).
        context = super().get_context_data(**kwargs)
        context["letters"] = list(string.ascii_lowercase)
        context["selected_letter"] = self.kwargs.get("letter", "a")
        # Finally, return the context data.
        return context


# class BookListView(ListView):
#     template_name = "books/detail.html"
#     context_object_name = "object_list"
#     paginate_by = 2

#     def get_queryset(self):
#         # Get the slug parameter from the URL pattern. The slug parameter is
#         # the slug of the BookTitle object whose books we want to display.
#         title_slug = self.kwargs.get("slug")
#         # Get the BookTitle object with the given slug. If no BookTitle object
#         # exists with the given slug, 404.
#         book_title = get_object_or_404(BookTitle, slug=title_slug)
#         # Return a QuerySet of all the Book objects whose title is the
#         # BookTitle object we just retrieved.
#         return Book.objects.filter(title=book_title)


class BookTitleDetailView(DetailView):
    model = BookTitle
    template_name = "books/detail.html"


# def book_title_detail_view(request: HttpRequest, slug: str, letter: str) -> HttpResponse:
#     obj: BookTitle = get_object_or_404(BookTitle, slug=slug)
#     return render(request, "books/detail.html", {"obj": obj})

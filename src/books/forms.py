from django import forms
from django.core.exceptions import ValidationError

from .models import BookTitle


class BookTitleForm(forms.ModelForm):
    class Meta:
        model = BookTitle
        fields = [
            "publisher",
            "author",
            "title",
        ]

    def clean(self):
        title = self.cleaned_data.get("title")
        if len(title) < 5:
            msg = "Title must be at least 5 characters long."
            # self.add_error("title", msg)
            raise ValidationError(msg)

        book_title_exists = BookTitle.objects.filter(title__iexact=title).exists()
        if book_title_exists:
            raise ValidationError("This title already exists. Please enter a new one.")

        return self.cleaned_data

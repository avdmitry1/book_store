from django import forms

from .choices import FORMAT_CHOICES


class SearchBookForm(forms.Form):
    search = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Search by book id..."}),
        label="",
        required=False,  # Allows the field to be optional, preventing potential errors
    )


class SelectExportOptionForm(forms.Form):
    format = forms.ChoiceField(
        choices=FORMAT_CHOICES, widget=forms.RadioSelect, label="Format"
    )

from django import forms


class SearchBookForm(forms.Form):
    search = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Search by book id..."}),
        label="",
        required=False,  # Allows the field to be optional, preventing potential errors
    )


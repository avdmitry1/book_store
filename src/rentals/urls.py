from django.urls import path

from .views import BookRentalHistoryView, search_book_view

app_name = "rentals"
urlpatterns = [
    path("", search_book_view, name="main"),
    path("<str:book_id>/", BookRentalHistoryView.as_view(), name="detail"),
]

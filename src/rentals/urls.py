from django.urls import path

from .views import (
    BookRentalHistoryView,
    UpdateRentalStatusView,
    search_book_view,
    CreateNewRentalView,
)

app_name = "rentals"
urlpatterns = [
    path("", search_book_view, name="main"),
    path("<str:book_id>/", BookRentalHistoryView.as_view(), name="detail"),
    path("<str:book_id>/<pk>/", UpdateRentalStatusView.as_view(), name="update"),
    path("<str:book_id>/new", CreateNewRentalView.as_view(), name="new"),
]

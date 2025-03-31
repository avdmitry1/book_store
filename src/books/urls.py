from django.urls import path

from .views import (BookDeleteView, BookDetailView, BookTitleDetailView,
                    BookTitleListView)

app_name = "books"

urlpatterns = [
    path("", BookTitleListView.as_view(), name="main"),
    path("<str:letter>/", BookTitleListView.as_view(), name="main"),
    path("<str:letter>/<slug:slug>/", BookTitleDetailView.as_view(), name="detail"),
    path(
        "<str:letter>/<slug:slug>/<str:book_id>/",
        BookDetailView.as_view(),
        name="detail_book",
    ),
    path(
        "<str:letter>/<slug:slug>/<str:book_id>/delete",
        BookDeleteView.as_view(),
        name="delete_book",
    ),
]

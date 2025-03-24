from django.urls import path

from .views import BookTitleListView, BookTitleDetailView

app_name = "books"

urlpatterns = [
    path("", BookTitleListView.as_view(), name="main"),
    path("<str:letter>/", BookTitleListView.as_view(), name="main"),
    path("<str:letter>/<slug:slug>/", BookTitleDetailView.as_view(), name="detail"),
]

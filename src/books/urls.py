from django.urls import path

from .views import BookListView, BookTitleListView

app_name = "books"

urlpatterns = [
    path("", BookTitleListView.as_view(), name="main"),
    path("<str:letter>/", BookTitleListView.as_view(), name="main"),
    path("<str:letter>/<slug:slug>/", BookListView.as_view(), name="detail"),
]

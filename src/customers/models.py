from django.db import models
from django.utils.text import slugify

from books.models import Book


class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    user_name = models.CharField(max_length=100, blank=True, unique=True)
    additional_info = models.TextField(blank=True)
    rating = models.PositiveIntegerField(default=50)
    books = models.ManyToManyField(Book, blank=True, help_text="Select a book")
    book_count = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return str(self.user_name)

    def save(self, *args, **kwargs):
        """
        Save the customer to the database.

        If the customer doesn't have a username, generate one using the first and
        last name. Make sure the username is unique.
        """
        if not self.user_name:
            base_username = slugify(f"{self.first_name} {self.last_name}")
            unique_username = base_username

            counter = 1
            while Customer.objects.filter(user_name=unique_username).exists():
                unique_username = f"{base_username}{counter}"  # append counter
                counter += 1
            self.user_name = unique_username

        super().save(*args, **kwargs)

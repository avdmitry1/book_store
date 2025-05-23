from datetime import timedelta

from django.db import models

from books.models import Book
from customers.models import Customer

from .choices import STATUS_CHOICES


class Rental(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default="0")
    rent_start_date = models.DateField(help_text="Rental start date")
    rent_end_date = models.DateField(help_text="Rental deadline", blank=True)
    return_date = models.DateField(help_text="Return date", blank=True, null=True)
    is_closed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def status_text(self):
        return dict(STATUS_CHOICES).get(self.status)

    def __str__(self):
        return f"{self.book.isbn} rented by {self.customer.user_name}"

    def save(self, *args, **kwargs):
        if not self.rent_end_date:
            self.rent_end_date = self.rent_start_date + timedelta(days=14)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ("-created_at",)

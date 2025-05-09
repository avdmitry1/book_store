import uuid
from io import BytesIO

import qrcode
from django.core.files import File
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from authors.models import Author
from publishers.models import Publisher
from rentals.choices import STATUS_CHOICES

from .utils import hash_book_info


class BookTitle(models.Model):
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(blank=True)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @property
    def books(self):
        # This is a property method that allows access to related Book objects
        # through the book_set manager. It returns all Book instances that are
        # associated with this BookTitle instance.
        return self.book_set.all()

    def get_absolute_url(self):
        # Extract the first letter of the title and convert it to lowercase.
        letter = self.title[0].lower()
        context = {"letter": letter, "slug": self.slug}
        return reverse("books:detail", kwargs=context)

    def __str__(self):
        return f"Book: {self.title}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            # The slugify function takes a string and returns a URL-safe
            # version of it. It replaces spaces with hyphens, removes any
            # non-alphanumeric characters, and lowercases the string.
        super().save(*args, **kwargs)


class Book(models.Model):
    id = models.CharField(
        primary_key=True,
        unique=True,
        max_length=36,
        default=uuid.uuid4,
        editable=False,
    )
    title = models.ForeignKey(BookTitle, on_delete=models.CASCADE)
    isbn = models.CharField(max_length=255, blank=True)
    qr_code = models.ImageField(upload_to="qr_codes/", blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        # Extract the first letter of the title and convert it to lowercase.
        letter = self.title.title[0].lower()
        context = {
            "letter": letter,
            "slug": self.title.slug,
            "book_id": self.id,
        }
        return reverse("books:detail_book", kwargs=context)

    def delete_object(self):
        letter = self.title.title[0].lower()
        context = {
            "letter": letter,
            "slug": self.title.slug,
            "book_id": self.id,
        }
        return reverse("books:delete_book", kwargs=context)

    def __str__(self):
        return str(self.title)

    # obj.status замість obj.status()
    @property
    def status(self):
        # зберігаємо перший об'єкт,
        rental = self.rental_set.first()
        if not rental:
            return False
        return dict(STATUS_CHOICES).get(rental.status, "Невідомий статус")

    @property
    def rental_id(self):
        if len(self.rental_set.all()) > 0:
            return self.rental_set.first().id
        return None

    @property
    def is_available(self):
        rentals = self.rental_set.all()
        if rentals:
            return rentals.first().status == "1"
        return True

    def save(self, *args, **kwargs):
        """Generates ISBN and QR code before saving the book."""
        if not self.isbn:
            # self.isbn = str(uuid.uuid4()).replace("-", "")[:24].lower()
            self.isbn = hash_book_info(self.title.title, self.title.publisher.name)

            # Generate QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(self.isbn)
            qr.make(fit=True)

            qr_img = qr.make_image(fill_color="black", back_color="white")

            # Save the QR code to a file
            fname = f"qr_code-{self.isbn}.png"
            buffer = BytesIO()
            qr_img.save(buffer, format="PNG")  # Directly save the QR code image
            self.qr_code.save(fname, File(buffer), save=False)  # Save QR code file
            buffer.close()

            super().save(*args, **kwargs)

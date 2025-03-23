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
        letter = self.title[0].lower()
        return reverse("books:detail", kwargs={"letter": letter, "slug": self.slug})

    def __str__(self):
        return f"Book: {self.title}"

    def save(self, *args, **kwargs):
        """Sets the slug before saving."""
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Book(models.Model):
    title = models.ForeignKey(BookTitle, on_delete=models.CASCADE)
    isbn = models.CharField(max_length=255, blank=True)
    qr_code = models.ImageField(upload_to="qr_codes/", blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.title)

    @property
    def status(self):
        """Returns the rental status of the book."""
        if len(self.rental_set.all()) > 0:
            statuses = dict(STATUS_CHOICES)
            return statuses[self.rental_set.first().status]
        return False

    def save(self, *args, **kwargs):
        """Generates ISBN and QR code before saving the book."""
        if not self.isbn:
            self.isbn = str(uuid.uuid4()).replace("-", "")[:24].lower()

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

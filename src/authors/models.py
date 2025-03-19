from django.db import models


class Author(models.Model):
    """Book Author"""

    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"

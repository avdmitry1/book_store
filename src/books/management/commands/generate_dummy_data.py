import random
from typing import Any, Dict, List

from django.core.management.base import BaseCommand

from authors.models import Author
from books.models import Book, BookTitle
from customers.models import Customer
from publishers.models import Publisher


class Command(BaseCommand):
    """Generate dummy data for the books app"""
    help = __doc__

    def handle(self, *args: Any, **kwargs: Any) -> None:
        self.generate_authors()
        self.generate_publishers()
        self.generate_book_titles()
        self.generate_books()
        self.generate_customers()

    def generate_authors(self) -> None:
        author_names = ["John Smith", "Jane Doe", "Bob Johnson", "Alice Clark"]
        for name in author_names:
            Author.objects.get_or_create(name=name)

    def generate_publishers(self) -> None:
        publishers: List[Dict[str, str]] = [
            {"name": "X books", "country": "US"},
            {"name": "Books", "country": "DE"},
            {"name": "Edu Mind", "country": "GB"},
            {"name": "Next", "country": "PL"},
        ]
        for publisher in publishers:
            Publisher.objects.get_or_create(**publisher)

    def generate_book_titles(self) -> None:
        titles = [
            "Harry Potter and the Philosopher's Stone",
            "Lord of the Rings",
            "Django Made Easy",
            "Web Development",
        ]
        authors: List[Author] = list(Author.objects.all())
        publishers: List[Publisher] = list(Publisher.objects.all())
        if not authors or not publishers:
            return

        for title in titles:
            author: Author = random.choice(authors)
            publisher: Publisher = random.choice(publishers)
            BookTitle.objects.update_or_create(
                title=title, defaults={"author": author, "publisher": publisher}
            )

    def generate_books(self) -> None:
        book_titles: List[BookTitle] = list(BookTitle.objects.all())
        for book_title in book_titles:
            quantity: int = random.randint(1, 5)
            for _ in range(quantity):
                Book.objects.get_or_create(title=book_title)

    def generate_customers(self) -> None:
        customers: List[Dict[str, str]] = [
            {"first_name": "John", "last_name": "Doe"},
            {"first_name": "Adam", "last_name": "Harris"},
            {"first_name": "Lisa", "last_name": "Martinez"},
        ]
        for customer in customers:
            Customer.objects.get_or_create(**customer)


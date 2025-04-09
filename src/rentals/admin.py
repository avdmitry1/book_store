from django.contrib import admin
from import_export import resources
from import_export.admin import ExportActionMixin
from import_export.fields import Field

from .choices import STATUS_CHOICES
from .models import Rental


class RentalResource(resources.ModelResource):
    book = Field()
    book_id = Field()
    isbn = Field()
    status = Field()
    is_closed = Field()
    customer = Field()

    class Meta:
        model = Rental
        fields = (
            "id",
            "book",
            "book_id",
            "isbn",
            "customer",
            "status",
            "rent_start_date",
            "rent_end_date",
            "return_date",
            "is_closed",
        )

    def dehydrate_book(self, obj):
        return obj.book.title.title

    def dehydrate_book_id(self, obj):
        return obj.book.id

    def dehydrate_isbn(self, obj):
        return obj.book.isbn

    def dehydrate_status(self, obj):
        statuses = dict(STATUS_CHOICES)
        return statuses.get(obj.status)

    def dehydrate_is_closed(self, obj):
        return True if obj.is_closed == 1 else False

    def dehydrate_customer(self, obj):
        return obj.customer.user_name


class RentalAdmin(ExportActionMixin, admin.ModelAdmin):
    resource_class = RentalResource


admin.site.register(Rental, RentalAdmin)

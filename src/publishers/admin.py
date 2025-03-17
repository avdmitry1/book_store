from django.contrib import admin
from import_export import resources
from import_export.admin import ExportActionMixin
from import_export.fields import Field

from .models import Publisher


class PublisherResource(resources.ModelResource):
    created = Field(attribute="created", column_name="created")

    class Meta:
        model = Publisher
        fields = ("id", "name", "country", "created")
        export_ordered = ("id", "name", "country", "created")

    def dehydrate_created(self, obj):
        return obj.created.strftime("%Y-%m-%d")


class PublisherAdmin(ExportActionMixin, admin.ModelAdmin):
    resource_class = PublisherResource


admin.site.register(Publisher, PublisherAdmin)


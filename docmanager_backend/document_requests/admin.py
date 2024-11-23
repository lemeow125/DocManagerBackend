from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import DocumentRequestUnit, DocumentRequest
from unfold.contrib.filters.admin import RangeDateFilter

# Register your models here.


@admin.register(DocumentRequestUnit)
class DocumentRequestUnitAdmin(ModelAdmin):
    search_fields = ["id"]
    list_display = ["id", "get_document_title", "copies"]

    def get_document_title(self, obj):
        return obj.document.name

    get_document_title.short_description = "Document"


@admin.register(DocumentRequest)
class DocumentRequestAdmin(ModelAdmin):
    list_filter = [
        ("date_requested", RangeDateFilter),
    ]

    list_display = ["id", "date_requested", "status", "college"]

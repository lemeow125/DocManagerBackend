from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Document


@admin.register(Document)
class DocumentAdmin(ModelAdmin):
    model = Document
    search_fields = ["id", "name", "subject", "sent_from", "document_year",
                     "document_month", "document_type"]
    list_display = ["id", "name", "subject", "sent_from", "document_year",
                    "document_month", "document_type", "date_uploaded"]

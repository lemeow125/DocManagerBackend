from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Document


@admin.register(Document)
class DocumentAdmin(ModelAdmin):
    model = Document
    search_fields = ["id", "name", "document_type"]
    list_display = ["id", "name", "document_type", "date_uploaded"]

from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Notification
from unfold.contrib.filters.admin import RangeDateFilter

# Register your models here.


@admin.register(Notification)
class NotificationAdmin(ModelAdmin):
    search_fields = ["id"]
    list_display = ["id", "content", "type", "timestamp", "audience", "client"]

    list_filter = [
        ("timestamp", RangeDateFilter),
    ]

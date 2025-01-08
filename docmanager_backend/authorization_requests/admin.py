from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import AuthorizationRequest

# Register your models here.


@admin.register(AuthorizationRequest)
class AuthorizationRequestAdmin(ModelAdmin):
    search_fields = ["id"]
    list_display = ["id", "date_requested", "status", "college"]

from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Questionnaire


@admin.register(Questionnaire)
class QuestionnaireAdmin(ModelAdmin):
    model = Questionnaire
    search_fields = ["id", "date_submitted"]
    list_display = ["id", "date_submitted"]

from django.urls import include, path
from .views import (
    QuestionnaireListAPIView,
    QuestionnaireSubmitView,
)

urlpatterns = [
    path("submit/", QuestionnaireSubmitView.as_view()),
    path("list/", QuestionnaireListAPIView.as_view()),
]

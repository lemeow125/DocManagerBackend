from django.urls import path, include
from .views import (
    DocumentRequestCreateView,
    DocumentRequestListView,
    DocumentRequestUpdateView,
)

urlpatterns = [
    path("create/", DocumentRequestCreateView.as_view()),
    path("list/", DocumentRequestListView.as_view()),
    path("update/<int:pk>/", DocumentRequestUpdateView.as_view()),
]

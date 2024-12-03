from django.urls import path, include
from .views import (
    DocumentRequestCreateView,
    DocumentRequestListView,
    DocumentRequestUpdateView,
    DocumentRequestFullListView,
)

urlpatterns = [
    path("create/", DocumentRequestCreateView.as_view()),
    path("list/", DocumentRequestListView.as_view()),
    path("list/head/", DocumentRequestFullListView.as_view()),
    path("update/<int:pk>/", DocumentRequestUpdateView.as_view()),
]

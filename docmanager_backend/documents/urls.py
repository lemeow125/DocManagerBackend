from django.urls import include, path
from .views import (
    DocumentUploadView,
    DocumentDeleteView,
    DocumentListView,
    DocumentStaffListView,
    DocumentUpdateView
)

urlpatterns = [
    path("upload/", DocumentUploadView.as_view()),
    path("update/<int:pk>/", DocumentUpdateView.as_view()),
    path("delete/<int:pk>/", DocumentDeleteView.as_view()),
    path("list/", DocumentListView.as_view()),
    path("list/staff/", DocumentStaffListView.as_view()),
]

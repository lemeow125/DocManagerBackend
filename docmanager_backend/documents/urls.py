from django.urls import include, path
from .views import (
    DocumentUploadView,
    DocumentDeleteView,
    DocumentListView,
    DocumentStaffListView,
)

urlpatterns = [
    path("upload/", DocumentUploadView.as_view()),
    path("delete/<int:pk>/", DocumentDeleteView.as_view()),
    path("list/", DocumentListView.as_view()),
    path("list/staff/", DocumentStaffListView.as_view()),
]

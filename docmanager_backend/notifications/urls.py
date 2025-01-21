from django.urls import path
from .views import (
    NotificationListView,
    NotificationDeleteView
)

urlpatterns = [
    path("list/", NotificationListView.as_view()),
    path("delete/<int:pk>/", NotificationDeleteView.as_view()),
]

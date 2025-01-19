from django.urls import path, include
from .views import (
    AuthorizationRequestCreateView,
    AuthorizationRequestUpdateView,
    AuthorizationRequestListView,
    AuthorizationRequestUnitUpdateView
)

urlpatterns = [
    path("create/", AuthorizationRequestCreateView.as_view()),
    path("list/", AuthorizationRequestListView.as_view()),
    path("update/<int:pk>/", AuthorizationRequestUpdateView.as_view()),
    path("authorization_request_units/update/<int:pk>/",
         AuthorizationRequestUnitUpdateView.as_view()),
]

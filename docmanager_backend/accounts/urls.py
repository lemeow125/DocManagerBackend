from django.urls import include, path
from .views import CustomUserDeleteView

urlpatterns = [
    path("", include("djoser.urls")),
    path("", include("djoser.urls.jwt")),
    path("users/delete/<int:pk>/", CustomUserDeleteView.as_view()),
]

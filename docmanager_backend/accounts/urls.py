from django.urls import include, path
from .views import CustomUserDeleteView, CustomUserUpdateView

urlpatterns = [
    path("", include("djoser.urls")),
    path("", include("djoser.urls.jwt")),
    path("users/delete/<int:pk>/", CustomUserDeleteView.as_view()),
    path("users/update/<int:pk>/", CustomUserUpdateView.as_view()),
]

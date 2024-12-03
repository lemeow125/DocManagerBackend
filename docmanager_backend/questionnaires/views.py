from rest_framework import generics
from .serializers import QuestionnaireSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Questionnaire
from rest_framework.pagination import PageNumberPagination
from accounts.permissions import IsStaff, IsPlanning


class QuestionnaireListAPIView(generics.ListAPIView):
    """
    Used by staff to view questionnaires
    """

    http_method_names = ["get"]
    serializer_class = QuestionnaireSerializer
    queryset = Questionnaire.objects.all()
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticated, IsPlanning]


class QuestionnaireSubmitView(generics.CreateAPIView):
    """
    Used by clients to submit questionnaires
    """

    http_method_names = ["post"]
    serializer_class = QuestionnaireSerializer
    permission_classes = [IsAuthenticated]

from rest_framework import generics

from problems_list.serializers import AllProblemsListSerializer
from topics.models import Problem


class AllProblemsListView(generics.ListAPIView):
    # permission_classes = (IsAuthenticated, )
    serializer_class = AllProblemsListSerializer
    queryset = Problem.objects.all()


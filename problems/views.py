from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from problems.serializers import ProblemSerializer
from topics.models import Problem


class ProblemView(generics.RetrieveAPIView):  # here I'll need to return everything about problem
    # permission_classes = (IsAuthenticated, )
    serializer_class = ProblemSerializer

    def get_queryset(self):
        return Problem.objects.filter(id=self.kwargs['pk'])

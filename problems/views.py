from collections import defaultdict

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.utils import json

from problems.serializers import ProblemSerializer, ImagesForProblemSerializer, SubmitProblemSerializer
from topics.models import Problem


class ProblemView(generics.RetrieveAPIView):
    # permission_classes = (IsAuthenticated, )
    serializer_class = ProblemSerializer

    def get_queryset(self):
        return Problem.objects.filter(id=self.kwargs['pk'])


class SubmitProblemView(generics.GenericAPIView):  # 0.0 == 0
    # permission_classes = (IsAuthenticated, )
    serializer_class = SubmitProblemSerializer

    def post(self, request, pk, **kwargs):
        queryset = Problem.objects.filter(id=pk)
        user_answer = json.loads(request.body)
        if queryset.values()[0]['answer'] != user_answer['answer']:
            return Response({"message": "Wrong Answer"})
        return Response({"message": "Accepted"})

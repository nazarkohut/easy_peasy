from collections import defaultdict

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.utils import json

from misc.converters import custom_response_with_lists
from problems.serializers import ProblemSerializer, SubmitProblemSerializer, \
    AllProblemsListSerializer
from topics.models import Problem


class AllProblemsListView(generics.ListAPIView):
    # permission_classes = (IsAuthenticated, )
    serializer_class = AllProblemsListSerializer
    queryset = Problem.objects.all()


class ProblemView(generics.RetrieveAPIView):
    # permission_classes = (IsAuthenticated, )
    serializer_class = ProblemSerializer

    def get_queryset(self):
        return Problem.objects.filter(id=self.kwargs['pk'])

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        data = custom_response_with_lists(data=data, first_level=('images', 'tags'), second_level=('image', 'tag'))
        return Response(data)


class SubmitProblemView(generics.GenericAPIView):  # 0.0 == 0
    # permission_classes = (IsAuthenticated, )
    serializer_class = SubmitProblemSerializer

    def post(self, request, pk, **kwargs):
        queryset = Problem.objects.filter(id=pk)
        user_answer = json.loads(request.body)
        if queryset.values()[0]['answer'] != user_answer['answer']:
            return Response({"message": "Wrong Answer"})
        return Response({"message": "Accepted"})

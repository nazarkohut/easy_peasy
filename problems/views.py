from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.utils import json

from misc.converters import custom_response_with_lists
from problems.models import Problem
from problems.serializers import ProblemSerializer, SubmitProblemSerializer, \
    AllProblemsListSerializer


class AllProblemsListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
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


class SubmitProblemView(generics.GenericAPIView):
    # permission_classes = (IsAuthenticated, )
    serializer_class = SubmitProblemSerializer

    def put(self, request, pk, **kwargs):
        queryset = Problem.objects.filter(id=pk)
        user_answer = json.loads(request.body)
        data = queryset.values()[0]
        self.get_serializer().validate(user_answer)
        if data['answer'] != user_answer['answer']:
            self.increment_problem_fields(queryset, data, is_correct_answer=False)
            return Response({"message": "Wrong Answer"})
        self.increment_problem_fields(queryset, data, is_correct_answer=True)
        return Response({"message": "Accepted"})

    @staticmethod
    def increment_problem_fields(queryset, data, is_correct_answer):
        del data['answer']
        data['attempts'] += 1
        data['accepted'] = data['accepted'] + 1 if is_correct_answer else data['accepted']
        queryset.update(**data)

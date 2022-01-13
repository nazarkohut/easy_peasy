from collections import defaultdict

from django.db.models import F
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.utils import json

from misc.converters import list_of_dicts_to_one_dict
from tests.models import Test, ProblemTest
from tests.serializers import AllTestListSerializer, TestSerializer, SubmitTestSerializer
from topics.models import Problem


class AllTestsListView(generics.ListAPIView):
    # permission_classes = (IsAuthenticated, ) # I may change permissions later
    serializer_class = AllTestListSerializer

    def get_queryset(self):
        return Test.objects.all()


class TestView(generics.RetrieveAPIView):
    # permission_classes = (IsAuthenticated, )
    serializer_class = TestSerializer

    def get_queryset(self):
        return Test.objects.filter(id=self.kwargs['pk'])


class SubmitTestView(generics.GenericAPIView):  # this one is incomplete
    # permission_classes = (IsAuthenticated, )
    serializer_class = SubmitTestSerializer

    def put(self, request, pk, **kwargs):
        # queryset = ProblemTest.objects.select_related("problem").filter(test_id=pk)
        queryset = Problem.objects.prefetch_related('problemtest_set').filter(problemtest__test_id=pk)
        user_answers = json.loads(request.body)
        data = list_of_dicts_to_one_dict(lst=queryset.values(), key_param='id', value_param='answer')
        response = list()
        for k in data.keys():
            curr = defaultdict(str)
            curr['id'] = k
            problem_id = str(k)  # from database =)
            if problem_id in user_answers:
                if data[k] == user_answers[problem_id]:
                    curr['message'] = 'Accepted'
                else:
                    curr['message'] = 'Wrong Answer'
            else:
                curr['message'] = 'Wrong Answer'
            response.append(curr)

        # response= {{'id': 1, 'message': 'Accepted', 'points': 1}, {'id': 3, 'message': Fail, 'points': 0}}
        return Response(response)
        # Select * from ProblemTest pt inner join Problem p on pt.problem_id=p.id where test_id=pk;

from collections import defaultdict

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.utils import json

from misc.converters import list_of_dicts_to_one_dict
from tests.models import Test, ProblemTest, TestResult
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
        cost_queryset = ProblemTest.objects.select_related("problem").filter(test_id=pk)
        queryset = Problem.objects.prefetch_related('problemtest_set').filter(problemtest__test_id=pk)
        user_answers = json.loads(request.body)
        # converting query sets to convenient representation
        costs = list_of_dicts_to_one_dict(cost_queryset.values(), key_param='problem_id', value_param='cost')
        data = list_of_dicts_to_one_dict(lst=queryset.values(), key_param='id', value_param='answer')
        # data validation starts here
        response, general_mark = self._check_test_answers(correct_answers=data, user_answers=user_answers, costs=costs)
        self.insert_row_to_test_result(data=response, mark=general_mark)
        return Response(response, status=200)

    @staticmethod
    def insert_row_to_test_result(data: list, mark: int):
        test_result = TestResult(mark=mark, problems_info=data)  # need to relate user_profile
        test_result.save(force_insert=True)

    @staticmethod
    def _check_test_answers(correct_answers: dict, costs: dict, user_answers: dict) -> [list, int]:
        def invalid_answer(d: dict) -> dict:
            d['message'] = 'Wrong Answer'
            d['mark'] = '0'
            return d

        def valid_answer(d: dict, mark_counter: int) -> [dict, int]:
            curr['message'] = 'Accepted'
            curr['mark'] = str(costs[k])
            mark_counter += costs[k]
            return [d, mark_counter]

        res = list()
        general_mark = 0
        for k in correct_answers.keys():
            curr = defaultdict(str)
            curr['id'] = k
            problem_id = str(k)  # from database =)
            if problem_id in user_answers:
                if correct_answers[k] == user_answers[problem_id]:
                    curr, general_mark = valid_answer(curr, general_mark)
                else:
                    curr = invalid_answer(curr)
            else:
                curr = invalid_answer(curr)
            res.append(curr)
        return [res, general_mark]

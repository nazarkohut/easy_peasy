from collections import defaultdict

from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.utils import json

from misc.converters import list_of_dicts_to_one_dict
from tests.models import Test, ProblemTest, TestResult
from tests.serializers import AllTestListSerializer, TestSerializer, SubmitTestSerializer
from topics.models import Problem
from users.models import UserProfile


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


class SubmitTestView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = SubmitTestSerializer

    def put(self, request, pk, **kwargs):
        cost_queryset = ProblemTest.objects.select_related("problem").filter(test_id=pk)
        queryset = Problem.objects.prefetch_related('problemtest_set').filter(problemtest__test_id=pk)
        body = json.loads(request.body)
        self.get_serializer().validate(attrs=body)
        # converting query sets to convenient representation
        user_answers = list_of_dicts_to_one_dict(lst=body, key_param='id', value_param='answer')
        costs = list_of_dicts_to_one_dict(lst=cost_queryset.values(), key_param='problem_id', value_param='cost')
        data = list_of_dicts_to_one_dict(lst=queryset.values(), key_param='id', value_param='answer')
        # determining which answer was correct starts here (under this line)
        response, general_mark = self.check_test_answers(correct_answers=data, user_answers=user_answers, costs=costs)
        self.insert_row_to_test_result(data=response, mark=general_mark, user_id=request.user.id)
        return Response(response, status=200)

    @staticmethod
    def insert_row_to_test_result(data: list, mark: int, user_id: int):
        profile = UserProfile.objects.get(user_id=user_id)
        test_result = TestResult(mark=mark, problems_info=data, user_profile=profile)
        test_result.save(force_insert=True)

    @staticmethod
    def check_test_answers(correct_answers: dict, costs: dict, user_answers: dict) -> [list, int]:
        def invalid_answer(d: dict) -> dict:
            d['message'] = 'Wrong Answer'
            d['mark'] = '0'
            return d

        def valid_answer(d: dict, mark_counter: int) -> [dict, int]:
            d['message'] = 'Accepted'
            d['mark'] = str(costs[k])
            mark_counter += costs[k]
            return [d, mark_counter]

        def not_answered_question(d: dict) -> dict:
            d['message'] = 'Skipped'
            d['mark'] = '0'
            return d

        res = list()
        general_mark = 0
        # print(correct_answers, user_answers)
        for k in correct_answers.keys():
            curr = defaultdict(str)

            curr['id'] = k
            problem_id = k  # from database =)
            if problem_id in user_answers:
                if correct_answers[k] == user_answers[problem_id]:
                    curr, general_mark = valid_answer(curr, general_mark)
                else:
                    curr = invalid_answer(curr)
            else:
                curr = not_answered_question(curr)
            res.append(curr)
        return [res, general_mark]

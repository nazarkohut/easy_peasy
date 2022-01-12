from django.db.models import F
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

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
        return Response(queryset.values())
        # Select * from ProblemTest pt inner join Problem p on pt.problem_id=p.id where test_id=pk;

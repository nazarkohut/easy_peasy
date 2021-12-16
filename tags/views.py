from django.db.models import Count
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from tags.serializers import ProblemsSortedByTagsListSerializer
from topics.models import Problem


class ProblemsSortedByTagsListView(generics.ListAPIView):
    # permission_classes = (IsAuthenticated, )
    serializer_class = ProblemsSortedByTagsListSerializer

    def get_queryset(self):
        tag_id_list = self.request.query_params.get('tag_id')
        return Problem.objects.filter(tags__in=tag_id_list)
        # problem_list = Problem.objects.filter(tags__in=tag_id_list).all()  # still incomplete searches I have to search exact fields
        # for i in problem_list:
        #     print(i.__dict__)
        # # set(problem_list) ^ set(tag_id_list)
        # # print(problem_list)
        # return problem_list

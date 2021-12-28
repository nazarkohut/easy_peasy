from django.db.models import Count
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from misc.converters import custom_response_with_lists
from tags.serializers import ProblemsSortedByTagsListSerializer
from topics.models import Problem


class ProblemsSortedByTagsListView(generics.ListAPIView):
    # permission_classes = (IsAuthenticated, )
    serializer_class = ProblemsSortedByTagsListSerializer

    def get_queryset(self):  # Now work as it was expected
        tag_id_list = self.request.query_params.getlist('tag_id')
        return Problem.objects.filter(tags__in=tag_id_list).annotate(cnt=Count('tags', distinct=True)) \
            .filter(cnt=len(tag_id_list))

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        output = list()
        for i in self.get_serializer(queryset, many=True).data:
            current = i
            current = custom_response_with_lists(current, ('tags', ), ('tag', ))
            output.append(current)
        return Response(output, status=status.HTTP_200_OK)

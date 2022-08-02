from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from topics.models import Topic, Subtopic
from topics.serializers import SubtopicsListSerializer, ProblemsListForSubtopicSerializer
    # ProblemsListForTopicSerializer


class SubtopicsForTopicView(generics.ListAPIView):
    # permission_classes = (IsAuthenticated, )
    serializer_class = SubtopicsListSerializer
    queryset = Topic.objects.all()


class ProblemsListForSubtopicView(generics.ListAPIView):
    # permission_classes = (IsAuthenticated, )
    serializer_class = ProblemsListForSubtopicSerializer

    def get_queryset(self):
        return Subtopic.objects.filter(id=self.kwargs['pk'])

#
# class ProblemsListForTopicView(generics.ListAPIView):
#     serializer_class = ProblemsListForTopicSerializer
#
#     def get_queryset(self):
#         topic_id = self.kwargs['pk']
#         return Topic.objects.filter(id=topic_id).prefetch_related('sub_topics')

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from topics.models import Topic, Subtopic, Problem
from topics.serializers import SubtopicsListSerializer, ProblemsListSerializer


class SubtopicsForTopicView(generics.ListAPIView):
    # permission_classes = (IsAuthenticated, )
    serializer_class = SubtopicsListSerializer
    queryset = Topic.objects.all()


class ProblemsListView(generics.ListAPIView):
    # permission_classes = (IsAuthenticated, )
    serializer_class = ProblemsListSerializer

    def get_queryset(self):
        return Subtopic.objects.filter(id=self.kwargs['pk'])

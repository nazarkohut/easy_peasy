from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated

from topics.models import Topic, Subtopic, Problem
from topics.serializers import TopicListSerializer, SubtopicListSerializer, ProblemListSerializer


class TopicsListView(generics.ListAPIView):
    # permission_classes = (IsAuthenticated, )
    serializer_class = TopicListSerializer
    queryset = Topic.objects.all()


class SubtopicsListView(generics.ListAPIView):  # when smb click on topic he or she will see list of topics
    # permission_classes = (IsAuthenticated,)
    serializer_class = SubtopicListSerializer

    def get_queryset(self):     # add 404 later
        subtopic = Subtopic.objects.filter(topic_id=self.kwargs['pk'])
        return subtopic


class ProblemsListView(generics.ListAPIView):  # list of problems for certain subtopic
    # permission_classes = (IsAuthenticated,)
    serializer_class = ProblemListSerializer

    def get_queryset(self):

        problem = Problem.objects.filter(sub_topics__id=self.kwargs['pk'])  # this sorts objects as I want but return
        # all subtopics(I doknow if i need this feature)
        return problem



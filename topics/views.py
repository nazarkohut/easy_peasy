from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND

from topics.models import Topic, Subtopic, Problem
from topics.serializers import TopicListSerializer, SubtopicListSerializer, ProblemListSerializer


class TopicsListView(generics.ListAPIView):
    # permission_classes = (IsAuthenticated, )
    serializer_class = TopicListSerializer
    queryset = Topic.objects.all()
    Response(data=serializer_class.data, status=status.HTTP_200_OK)


class SubtopicsListView(generics.ListAPIView):  # when smb click on topic he or she will see list of topics
    # permission_classes = (IsAuthenticated,)
    serializer_class = SubtopicListSerializer

    def get_queryset(self):     # add 404 later
        subtopic = Subtopic.objects.filter(pk=self.kwargs['pk'])
        return subtopic


class ProblemsListView(generics.ListAPIView):  # list of problems for certain subtopic
    # permission_classes = (IsAuthenticated,)
    serializer_class = ProblemListSerializer

    def get_queryset(self):
        problem = Problem.objects.filter(pk=self.kwargs['pk'])
        return problem



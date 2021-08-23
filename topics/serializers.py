from rest_framework import serializers

from topics.models import Topic, Subtopic, Problem


class TopicListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'


class SubtopicListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subtopic
        fields = '__all__'
        depth = 2


class ProblemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = '__all__'
        depth = 1

from rest_framework import serializers
from topics.models import Problem, Tag


class ProblemSerializer(serializers.ModelSerializer):
    tags = serializers.ListSerializer(child=serializers.CharField())
    sub_topics = serializers.ReadOnlyField(source='sub_topics.topic')

    class Meta:
        model = Problem
        fields = ('id', 'task', 'sub_topics', 'tags', )
        depth = 1

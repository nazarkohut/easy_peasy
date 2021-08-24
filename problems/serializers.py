from rest_framework import serializers
from topics.models import Problem, Tag

class TagsForProblemSerializer(serializers.ModelSerializer):
    problems = serializers.ReadOnlyField(source='tags.problems')
    id = serializers.ReadOnlyField(source='tags')

    class Meta:
        model = Tag
        fields = '__all__'


class ProblemSerializer(serializers.ModelSerializer):
    tags = TagsForProblemSerializer(many=True)
    sub_topics = serializers.ReadOnlyField(source='sub_topics.topic')

    class Meta:
        model = Problem
        fields = ('id', 'task', 'sub_topics', 'tags', )
        depth = 1

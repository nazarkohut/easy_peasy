from rest_framework import serializers

from problems.models import Problem
from tags.models import Tag


class AllProblemsTagsListSerializer(serializers.ModelSerializer):
    # problems = serializers.ReadOnlyField(source='')
    id = serializers.ReadOnlyField(source='')

    class Meta:
        model = Tag
        fields = ('id', )


class TagsForSortedByTagsListSerializer(serializers.ModelSerializer):
    problems = serializers.ReadOnlyField(source='')

    class Meta:
        model = Tag
        fields = '__all__'


class ProblemsSortedByTagsListSerializer(serializers.ModelSerializer):
    tags = TagsForSortedByTagsListSerializer(many=True)
    sub_topics = serializers.ReadOnlyField(source='')
    condition = serializers.ReadOnlyField(source='')
    answer = serializers.ReadOnlyField(source='')

    class Meta:
        model = Problem
        fields = '__all__'


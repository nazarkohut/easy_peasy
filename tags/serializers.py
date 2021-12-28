from rest_framework import serializers

from topics.models import Problem, Tag


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


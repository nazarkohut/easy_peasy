from rest_framework import serializers

from topics.models import Problem


class AllProblemsListSerializer(serializers.ModelSerializer):
    sub_topics = serializers.ReadOnlyField(source='')

    class Meta:
        model = Problem
        fields = '__all__'

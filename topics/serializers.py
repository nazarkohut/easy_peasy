from rest_framework import serializers
from topics.models import Topic, Subtopic, Problem


# serializers for subtopics (They show all information about ALL subtopics and topics)
# -------------------------------------------------------------------------------

class SubtopicsForTopicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subtopic
        fields = ('id', 'name', )


class SubtopicsListSerializer(serializers.ModelSerializer):
    sub_topics = SubtopicsForTopicSerializer(many=True)

    class Meta:
        model = Topic
        fields = ('id', 'name', 'sub_topics')


# serializers for problems (They are responsible for problems in particular subtopic)
# -------------------------------------------------------------------------------

class ProblemsForSubtopicSerializer(serializers.ModelSerializer):
    sub_topics = serializers.ReadOnlyField(source='problems.sub_topics')

    class Meta:
        model = Problem
        fields = ('task', 'id', 'sub_topics', )


class ProblemsListSerializer(serializers.ModelSerializer):
    problems = ProblemsForSubtopicSerializer(many=True)

    class Meta:
        model = Subtopic
        fields = ('id', 'name', 'problems')
        depth = 1

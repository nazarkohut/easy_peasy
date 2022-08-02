from rest_framework import serializers

from problems.models import Problem
from topics.models import Topic, Subtopic


# serializers for problems (They are responsible for problems in particular subtopic)
# -------------------------------------------------------------------------------

class ProblemsForSubtopicSerializer(serializers.ModelSerializer):
    sub_topics = serializers.ReadOnlyField(source='problems.sub_topics')

    class Meta:
        model = Problem
        fields = ('task', 'id', 'sub_topics', 'complexity', 'accepted', 'attempts',)  # , 'images')


class ProblemsListForSubtopicSerializer(serializers.ModelSerializer):
    problems = ProblemsForSubtopicSerializer(many=True)

    class Meta:
        model = Subtopic
        fields = ('id', 'name', 'problems',)
        depth = 1


# serializers for subtopics (They show all information about ALL subtopics and topics)
# -------------------------------------------------------------------------------

class SubtopicsForTopicSerializer(serializers.ModelSerializer):
    problems = ProblemsForSubtopicSerializer(many=True)

    class Meta:
        model = Subtopic
        fields = ('id', 'name', 'problems')


#   gets all subtopics and problems for topic
class SubtopicsListSerializer(serializers.ModelSerializer):
    sub_topics = SubtopicsForTopicSerializer(many=True)

    class Meta:
        model = Topic
        fields = ('id', 'name', 'sub_topics')

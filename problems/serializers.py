from rest_framework import serializers

from topics.models import Problem, Tag, ProblemImage


# all problems
class AllProblemsListSerializer(serializers.ModelSerializer):
    sub_topics = serializers.ReadOnlyField(source='')
    answer = serializers.ReadOnlyField(source='')
    condition = serializers.ReadOnlyField(source='')

    class Meta:
        model = Problem
        fields = '__all__'


# particular problem
class ImagesForProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProblemImage
        fields = ('image', )


class TagsForProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('tag', )


class ProblemSerializer(serializers.ModelSerializer):
    tags = TagsForProblemSerializer(many=True)
    images = ImagesForProblemSerializer(many=True)

    class Meta:
        model = Problem
        fields = ('id', 'task', 'tags', 'complexity', 'accepted', 'attempts', 'condition', 'images', )
        depth = 1


# submit particular problem
class SubmitProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = ('answer', )

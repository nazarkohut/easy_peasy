from rest_framework import serializers

from topics.models import Problem, Tag, ProblemImage


class ImagesForProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProblemImage
        fields = ('images',)


class ProblemSerializer(serializers.ModelSerializer):
    tags = serializers.ListSerializer(child=serializers.CharField())  # gets str representation of Tag Object
    problem_image = ImagesForProblemSerializer(many=True)  # Have to be list of urls

    class Meta:
        model = Problem
        fields = ('id', 'task', 'tags', 'complexity', 'accepted', 'attempts', 'condition', 'problem_image')
        depth = 1


class SubmitProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = ('answer', )

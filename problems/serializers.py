from rest_framework import serializers

from misc.validators import find_missing

from problems.models import Problem, ProblemImage
from tags.models import Tag


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
        fields = ('image',)


class TagsForProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('tag',)


class ProblemSerializer(serializers.ModelSerializer):
    tags = TagsForProblemSerializer(many=True)
    images = ImagesForProblemSerializer(many=True)

    class Meta:
        model = Problem
        fields = ('id', 'task', 'tags', 'complexity', 'accepted', 'attempts', 'condition', 'images',)
        depth = 1


# submit particular problem
class SubmitProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = ('answer',)

    def validate(self, attrs):  # have to implement 1.275 and 1.26 validation
        missing = find_missing(self.fields, attrs)
        if missing:
            raise serializers.ValidationError(missing)
        answer = attrs['answer']
        if not isinstance(answer, float):
            raise serializers.ValidationError({"message": "Answer must be float"})
        return attrs

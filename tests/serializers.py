from rest_framework import serializers

from tests.models import Test
from topics.models import Problem


class AllTestListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = '__all__'


# ------
class ProblemsForTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = '__all__'


class TestSerializer(serializers.ModelSerializer):
    problem = ProblemsForTestSerializer

    class Meta:
        model = Test
        fields = '__all__'
        depth = 2


# -----------------------
class SubmitTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = '__all__'

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from misc.validators import check_fields
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

    def validate(self, attrs):
        if not isinstance(attrs, list):
            raise ValidationError(
                {"message": "Request body is not valid", "details": "Request body must be list of JSONs"})

        for item in attrs:
            if not isinstance(item, dict):
                raise ValidationError(
                    {"message": "Request body is not valid", "details": "Request body must be list of JSONs"})
            check_fields(fields=['id', 'answer'], data=item)
            
            if not isinstance(item['id'], int):
                raise ValidationError({"message": "id must be of type int"})
            if not isinstance(item['answer'], float):
                raise ValidationError({"message": "answer must be of type float"})


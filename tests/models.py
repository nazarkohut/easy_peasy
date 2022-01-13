import datetime

from django.db import models

from topics.models import Problem
from users.models import UserProfile


class Test(models.Model):
    name = models.CharField(max_length=64)
    user_profile = models.ManyToManyField(UserProfile, through="UserProfileTest")
    problem = models.ManyToManyField(Problem, through="ProblemTest")
    description = models.CharField(max_length=64)

    class Meta:
        db_table = "test"


class UserProfileTest(models.Model):
    test = models.ForeignKey(Test, on_delete=models.SET_NULL, null=True)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
    points = models.IntegerField(default=None)

    class Meta:
        db_table = "test_user_profile"


class ProblemTest(models.Model):
    test = models.ForeignKey(Test, on_delete=models.SET_NULL, null=True)
    problem = models.ForeignKey(Problem, on_delete=models.SET_NULL, null=True)
    cost = models.IntegerField()

    class Meta:
        db_table = "problem_test"


class TestResult(models.Model):  # results of previous tests
    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, related_name="previous_tests", null=True)
    mark = models.IntegerField()
    test_time = models.DateTimeField(auto_now_add=True)
    problems_info = models.JSONField()

    class Meta:
        db_table = "test_result"

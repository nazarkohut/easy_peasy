from django.db import models


class Topic(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Subtopic(models.Model):
    name = models.CharField(max_length=50)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='sub_topics')

    def __str__(self):
        return self.name


class Problem(models.Model):
    task = models.CharField(max_length=300)
    complexity = models.IntegerField(default=None)
    accepted = models.BigIntegerField(default=None)
    attempts = models.BigIntegerField(default=None)
    sub_topics = models.ManyToManyField(Subtopic, related_name='problems')

    def __str__(self):
        return self.task


class Task(models.Model):
    condition = models.TextField(max_length=1000)
    problem = models.OneToOneField(Problem, on_delete=models.CASCADE, related_name='problem', default=None)  # check this field

    def __str__(self):
        return self.condition


class Tag(models.Model):
    tag = models.CharField(max_length=30)
    problems = models.ManyToManyField(Problem, related_name='tags')

    def __str__(self):
        return self.tag

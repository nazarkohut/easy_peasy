from django.db import models


class Topic(models.Model):
    name = models.CharField(max_length=64)

    class Meta:
        db_table = "topic"

    def __str__(self):
        return self.name


class Subtopic(models.Model):
    name = models.CharField(max_length=64)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, related_name='sub_topics', null=True)

    class Meta:
        db_table = "subtopic"

    def __str__(self):
        return self.name


class Problem(models.Model):
    task = models.CharField(max_length=64, unique=True)
    complexity = models.IntegerField(default=None)
    accepted = models.BigIntegerField(default=None)
    attempts = models.BigIntegerField(default=None)
    sub_topics = models.ManyToManyField(Subtopic, related_name='problems')
    condition = models.TextField(max_length=1024)
    answer = models.FloatField(blank=False)

    class Meta:
        db_table = "problem"

    def __str__(self):
        return self.task


class ProblemImage(models.Model):
    image = models.ImageField(upload_to='images/', default='image_link')
    problem = models.ForeignKey(Problem, on_delete=models.SET_NULL, related_name="images", null=True)

    class Meta:
        db_table = "problem_image"


class Tag(models.Model):
    tag = models.CharField(max_length=64)
    problems = models.ManyToManyField(Problem, related_name='tags')

    class Meta:
        db_table = "tag"

    def __str__(self):
        return self.tag



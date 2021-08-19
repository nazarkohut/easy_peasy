from django.db import models

# Create your models here.


class Topic(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Subtopic(models.Model):
    name = models.CharField(max_length=50)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Problem(models.Model):
    task = models.CharField(max_length=300)
    sub_topics = models.ManyToManyField(Subtopic)

    def __str__(self):
        return self.task


class Tag(models.Model):
    tag = models.CharField(max_length=30)
    problems = models.ManyToManyField(Problem)

    def __str__(self):
        return self.tag

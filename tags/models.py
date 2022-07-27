from django.db import models

from problems.models import Problem


class Tag(models.Model):
    tag = models.CharField(max_length=64)
    problems = models.ManyToManyField(Problem, related_name='tags')

    class Meta:
        db_table = "tag"

    def __str__(self):
        return self.tag

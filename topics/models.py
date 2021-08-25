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
    sub_topics = models.ManyToManyField(Subtopic, related_name='problems')

    def __str__(self):
        return self.task

    # def get_absolute_url(self): # read about this
    #     """Returns the url to access a particular instance of the model."""
    #     return reverse('model-detail-view', args=[str(self.id)])


class Tag(models.Model):
    tag = models.CharField(max_length=30)
    problems = models.ManyToManyField(Problem, related_name='tags')

    def __str__(self):
        return self.tag

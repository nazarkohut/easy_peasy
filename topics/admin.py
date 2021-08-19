from django.contrib import admin

from topics.models import Topic, Subtopic, Problem, Tag

admin.site.register(Topic)
admin.site.register(Subtopic)
admin.site.register(Problem)
admin.site.register(Tag)

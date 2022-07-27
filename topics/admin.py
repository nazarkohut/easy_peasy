from django.contrib import admin

from problems.models import Problem, ProblemImage
from tags.models import Tag
from tests.admin import ProblemTestInline
from topics.models import Topic, Subtopic

admin.site.register(Topic)
admin.site.register(Subtopic)


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    inlines = (ProblemTestInline,)


admin.site.register(Tag)
admin.site.register(ProblemImage)

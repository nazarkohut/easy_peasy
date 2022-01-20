from django.contrib import admin

from tests.admin import ProblemTestInline
from topics.models import Topic, Subtopic, Problem, Tag, ProblemImage

admin.site.register(Topic)
admin.site.register(Subtopic)


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    inlines = (ProblemTestInline,)


admin.site.register(Tag)
# admin.site.register(Task)
admin.site.register(ProblemImage)

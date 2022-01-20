from django.contrib import admin

from tests.models import Test, ProblemTest


class ProblemTestInline(admin.TabularInline):
    model = ProblemTest
    extra = 1


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    inlines = (ProblemTestInline,)


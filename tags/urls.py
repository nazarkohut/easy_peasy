from django.urls import re_path, path

from tags.views import ProblemsSortedByTagsListView, AllProblemsTagsListView

urlpatterns = [
    path('all/', AllProblemsTagsListView.as_view(), name='all_problems_details'),
    re_path(r'^tag$', ProblemsSortedByTagsListView.as_view(), name='sorted_by_tags'),  # move this one to problems later
]

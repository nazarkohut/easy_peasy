from django.urls import re_path

from tags.views import ProblemsSortedByTagsListView

urlpatterns = [
    re_path(r'^tag$', ProblemsSortedByTagsListView.as_view(), name='sorted_by_tags'),
]

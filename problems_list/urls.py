from django.urls import path

from problems_list.views import AllProblemsListView

urlpatterns = [
    path('', AllProblemsListView.as_view(), name='all_problems'),
]

from django.urls import path

from topics.views import SubtopicsForTopicView, ProblemsListView

urlpatterns = [
    path('', SubtopicsForTopicView.as_view(), name='subtopics'),
    path('subtopic/<int:pk>/', ProblemsListView.as_view(), name='problems'),
]

from django.urls import path

from topics.views import SubtopicsForTopicView, ProblemsListForSubtopicView

urlpatterns = [
    path('', SubtopicsForTopicView.as_view(), name='subtopics'),
    path('subtopic/<int:pk>/', ProblemsListForSubtopicView.as_view(), name='subtopic_problems')
]

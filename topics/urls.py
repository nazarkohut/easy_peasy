from django.urls import path

from topics.views import TopicsListView, SubtopicsListView, ProblemsListView

urlpatterns = [
    path('', TopicsListView.as_view(), name='topics'),
    path('subtopic/<int:pk>/', SubtopicsListView.as_view(), name='subtopics'),
    path('problem/<int:pk>/', ProblemsListView.as_view(), name='problems'),
]

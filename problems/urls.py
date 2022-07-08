from django.urls import path

from problems.views import ProblemView, SubmitProblemView, AllProblemsListView

urlpatterns = [
    path('all/', AllProblemsListView.as_view(), name='all_problems'),
    path('<int:pk>/', ProblemView.as_view(), name='problem'),
    path('submit/<int:pk>/', SubmitProblemView.as_view(), name='submit_problem'),
]

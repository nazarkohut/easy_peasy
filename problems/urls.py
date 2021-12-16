from django.urls import path

from problems.views import ProblemView, SubmitProblemView

urlpatterns = [
    path('<int:pk>/', ProblemView.as_view(), name='problem'),
    path('submit/<int:pk>', SubmitProblemView.as_view(), name='submit_problem')
]

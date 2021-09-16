from django.urls import path

from problems.views import ProblemView

urlpatterns = [
    path('<int:pk>/', ProblemView.as_view(), name='problem'),
]

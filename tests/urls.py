from django.urls import path

from tests.views import AllTestsListView, TestView, SubmitTestView

urlpatterns = [
    path('all/', AllTestsListView.as_view(), name='tests'),
    path('<int:pk>/', TestView.as_view(), name='test'),
    path('submit/<int:pk>/', SubmitTestView.as_view(), name='submit_test'),
]

from django.urls import path
from .views import createFeedback, listFeedback, viewFeedback, viewStatistics

app_name = 'Feedback'

urlpatterns = [

    path('create/<int:eventoid>', createFeedback, name='create_feedback'),
    path('all/<int:eventoid>', listFeedback.as_view(), name='list_feedback'),
    path('view/<int:feedbackid>', viewFeedback, name='view_feedback'),
    path('statistics/<int:eventoid>', viewStatistics, name='view_feedback_statistics')

]

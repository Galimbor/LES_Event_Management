from django.urls import path
from .views import createFeedback, listFeedback, viewFeedback

app_name = 'Feedback'

urlpatterns = [

    path('create/<int:eventoid>', createFeedback, name='create_feedback'),
    path('all/<int:eventoid>', listFeedback.as_view(), name='list_feedback'),
    path('view/<int:feedbackid>', viewFeedback, name='view_feedback')

]

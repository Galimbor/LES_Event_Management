from django.urls import path
from .views import  createFeedback

app_name = 'Feedback'

urlpatterns = [

    path('create/<int:eventoid>', createFeedback, name='create_feedback'),
]

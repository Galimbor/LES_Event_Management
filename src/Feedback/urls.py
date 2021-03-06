from django.urls import path
from .views import createFeedback, listFeedback, viewFeedback, viewStatistics, deleteFeedback, listFeedbackProp, viewFeedbackProp, viewStatisticsProp, deleteFeedbackProp

app_name = 'Feedback'

urlpatterns = [

    path('create/<int:eventoid>', createFeedback, name='create_feedback'),
    path('all/<int:eventoid>', listFeedback.as_view(), name='list_feedback'),
    path('view/<int:feedbackid>', viewFeedback, name='view_feedback'),
    path('statistics/<int:eventoid>', viewStatistics, name='view_feedback_statistics'),
    path('delete/<int:feedbackid>', deleteFeedback, name='delete_feedback' ),

    path('allProp/<int:eventoid>', listFeedbackProp.as_view(), name='list_feedback_prop'),
    path('viewProp/<int:feedbackid>', viewFeedbackProp, name='view_feedback_prop'),
    path('statisticsProp/<int:eventoid>', viewStatisticsProp, name='view_feedback_statistics_prop'),
    path('deleteProp/<int:feedbackid>', deleteFeedbackProp, name='delete_feedback_prop'),

]

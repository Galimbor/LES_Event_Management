from django.urls import path
from .views import home_view

app_name = 'Evento'

urlpatterns = [

    path('views/', home_view, name='homeview'),
]

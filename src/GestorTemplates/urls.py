from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .views import FormList, FormCreate, FormDelete

urlpatterns = [
     path('', FormList.as_view(), name='form-list'),
     path('new', FormCreate.as_view(), name='create-form'),
     path('delete/<int:pk>', FormDelete.as_view(), name='delete-form'),
] 

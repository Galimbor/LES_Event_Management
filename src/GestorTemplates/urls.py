from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .views import FormList, FormCreate, delete_form

urlpatterns = [
     path('', FormList.as_view(), name='form-list'),
     path('new/<int:form_id>/<int:form_type>', FormCreate.as_view(), name='create-form'),
     path('delete/<int:pk>', delete_form, name='delete-form'),
] 

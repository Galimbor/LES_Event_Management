from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .views import FormList, FormCreate, FormUpdate, FormDelete

urlpatterns = [
     path('', FormList.as_view(), name='form-list'),
     path('new/<int:template_form_id>/<int:form_type>', FormCreate.as_view(), name='create-form'),
     path('edit/<int:pk>', FormUpdate.as_view(), name='edit-form'),
     path('delete/<int:pk>', FormDelete.as_view(), name='delete-form'),
] 

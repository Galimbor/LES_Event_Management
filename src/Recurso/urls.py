from django.urls import path, include
# from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .views import RecursoList, RecursoCreate, RecursoDelete

urlpatterns = [
    path('', RecursoList.as_view(), name='recurso-list'),
    path('new', RecursoCreate.as_view(), name='create-recurso'),
    path('delete/<int:pk>', RecursoDelete.as_view(), name='delete-recurso'),
]


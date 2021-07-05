from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .views import NotificacoesList, NotificacoesDelete, NotificacoesUpdate

urlpatterns = [
     path('', NotificacoesList.as_view(), name='notification-list'),
     path('estado/<int:estado>', NotificacoesList.as_view(), name='notification-list'),
     path('<int:pk>/', NotificacoesUpdate.as_view(), name='notification-update'),
     path('<int:pk>/delete', NotificacoesDelete.as_view(), name='notification-delete'),
] 

from django.urls import path, include
# from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# from .views import RecursoList, RecursoCreate, RecursoDelete
from Recurso.views import create_recurso, home_view, recursos, recurso_success

app_name = 'Recurso'

# urlpatterns = [
#     # path('', RecursoList.as_view(), name='recurso-list'),
#     # path('new', RecursoCreate.as_view(), name='create-recurso'),
#     # path('delete/<int:pk>', RecursoDelete.as_view(), name='delete-recurso'),
#
# ]

urlpatterns = [
    path('', home_view, name='homeview'),
    path('all/', recursos, name='recursos'),
    path('success/', recurso_success , name='recurso_success'),
    path('new/', create_recurso, name='create-recurso'),
]


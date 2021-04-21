from django.urls import path, include
# from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# from .views import RecursoList, RecursoCreate, RecursoDelete
from Recurso.views import recurso_create, recursos, recurso_detail, recurso_delete, espacos, equipamentos, servicos, \
    servico_create, equipamento_create, espaco_create

app_name = 'Recurso'

urlpatterns = [
    path('recurso', recursos, name='recursos'),
    path('espaco', espacos, name='espacos'),
    path('equipamento', equipamentos, name='equipamentos'),
    path('servico', servicos, name='servicos'),
    # path('success/', recurso_success, name='recurso-success'),
    path('recurso/recurso_create/', recurso_create, name='recurso-create'),
    path('recurso/<int:my_id>/', recurso_detail, name='recurso-detail'),
    path('recurso/<int:my_id>/delete/', recurso_delete, name='recurso-delete'),
    path('equip/equipamento_create/', equipamento_create, name='equipamento-create'),
    path('servico/servico_create/', servico_create, name='servico-create'),
    path('espaco/espaco_create/', espaco_create, name='espaco-create'),

]

from django.urls import path, include
# from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# from .views import RecursoList, RecursoCreate, RecursoDelete
from Recurso.views import recursos, recurso_detail, recurso_delete, espacos, empresas, edificios, unidadesorganicas, \
    equipamentos, servicos, servico_create, equipamento_create, espaco_create, equipamento_delete, empresa_create, \
    empresa_delete, edificio_create, edificio_delete, unidadeorganica_delete, unidadeorganica_create

app_name = 'Recurso'

urlpatterns = [
    path('recurso', recursos, name='recursos'),
    path('espaco', espacos, name='espacos'),
    path('equipamento', equipamentos, name='equipamentos'),
    path('servico', servicos, name='servicos'),
    path('empresa', empresas, name='empresas'),
    path('empresa', empresas, name='empresas'),
    path('edificio', edificios, name='edificios'),
    path('unidade-organica', unidadesorganicas, name='unidades-organicas'),
    # path('recurso/recurso_create/', recurso_create, name='recurso-create'),
    path('recurso/<int:my_id>/', recurso_detail, name='recurso-detail'),
    path('recurso/<int:my_id>/delete/', recurso_delete, name='recurso-delete'),
    path('equip/equipamento_create/', equipamento_create, name='equipamento-create'),
    path('servico/servico_create/', servico_create, name='servico-create'),
    path('espaco/espaco_create/', espaco_create, name='espaco-create'),
    path('equip/<int:my_id>/delete/', equipamento_delete, name='equipamento-delete'),
    path('empresa/empresa_create/', empresa_create, name='empresa-create'),
    path('edificio/edificio_create/', edificio_create, name='edificio-create'),
    path('unidade-organica/unidade-organica_create/', unidadeorganica_create, name='unidade-organica-create'),
    path('empresa/<int:my_id>/delete/', empresa_delete, name='empresa-delete'),
    path('edificio/<int:my_id>/delete/', edificio_delete, name='edificio-delete'),
    path('unidade-organica/<int:my_id>/delete/', unidadeorganica_delete, name='unidade-organica-delete'),

]

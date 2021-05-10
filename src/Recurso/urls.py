from django.urls import path, include
# from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# from .views import RecursoList, RecursoCreate, RecursoDelete
from Recurso.views import recursos, recurso_detail, recurso_delete, espacos, empresas, edificios, unidadesorganicas, \
    equipamentos, servicos, servico_create, equipamento_create, espaco_create, equipamento_delete, servico_delete, \
    empresa_create, empresa_delete, edificio_create, edificio_delete, unidadeorganica_delete, unidadeorganica_create, \
    universidades, universidade_create, universidade_delete, campis, campus_delete, campus_create, espaco_delete

app_name = 'Recurso'

urlpatterns = [
    path('recurso', recursos, name='recursos'),
    # path('recurso/recurso_create/', recurso_create, name='recurso-create'),
    path('recurso/<int:my_id>/', recurso_detail, name='recurso-detail'),
    path('recurso/<int:my_id>/delete/', recurso_delete, name='recurso-delete'),

    # ESPAÇO
    path('espaco', espacos, name='espacos'),
    path('espaco/espaco_create/', espaco_create, name='espaco-create'),
    path('equip/<int:my_id>/delete/', espaco_delete, name='espaco-delete'),

    # EQUIPAMENTOS
    path('equip', equipamentos, name='equipamentos'),
    path('equip/equipamento_create/', equipamento_create, name='equipamento-create'),
    path('equip/<int:my_id>/delete/', equipamento_delete, name='equipamento-delete'),

    # SERVIÇOS
    path('servico', servicos, name='servicos'),
    path('servico/servico_create/', servico_create, name='servico-create'),
    path('servico/<int:my_id>/delete/', servico_delete, name='servico-delete'),

    # EMPRESAS
    path('empresa', empresas, name='empresas'),
    path('empresa/empresa_create/', empresa_create, name='empresa-create'),
    path('empresa/<int:my_id>/delete/', empresa_delete, name='empresa-delete'),

    # EDIFICIOS
    path('edificio', edificios, name='edificios'),
    path('edificio/edificio_create/', edificio_create, name='edificio-create'),
    path('edificio/<int:my_id>/delete/', edificio_delete, name='edificio-delete'),

    # UNIDADE ORGANICA
    path('unidade-organica', unidadesorganicas, name='unidades-organicas'),
    path('unidade-organica/unidade-organica_create/', unidadeorganica_create, name='unidade-organica-create'),
    path('unidade-organica/<int:my_id>/delete/', unidadeorganica_delete, name='unidade-organica-delete'),

    # UNIDADE ORGANICA
    path('unidade-organica', unidadesorganicas, name='unidades-organicas'),
    path('unidade-organica/unidade-organica_create/', unidadeorganica_create, name='unidade-organica-create'),
    path('unidade-organica/<int:my_id>/delete/', unidadeorganica_delete, name='unidade-organica-delete'),

    # UNIVERSIDADE
    path('universidade', universidades, name='universidades'),
    path('universidade/universidade_create/', universidade_create, name='universidade-create'),
    path('universidade/<int:my_id>/delete/', universidade_delete, name='universidade-delete'),

    # CAMPUS
    path('campus', campis, name='campis'),
    path('campus/campus_create/', campus_create, name='campus-create'),
    path('campus/<int:my_id>/delete/', campus_delete, name='campus-delete'),

]

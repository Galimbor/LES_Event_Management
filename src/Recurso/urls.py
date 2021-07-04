from django.urls import path, include
# from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# from .views import RecursoList, RecursoCreate, RecursoDelete
from Recurso.views import recursos, recursosv2, recurso_detail, recurso_delete, espacos, empresas, edificios, \
    unidadesorganicas, \
    equipamentos, servicos, servico_create, equipamento_create, espaco_create, equipamento_delete, servico_delete, \
    empresa_create, empresa_delete, edificio_create, edificio_delete, unidadeorganica_delete, unidadeorganica_create, \
    universidades, universidade_create, universidade_delete, campis, campus_delete, campus_create, espaco_delete, \
    servico_detail, equipamento_detail, empresa_detail, unidadeorganica_update, unidadeorganica_detail, \
    universidade_detail, campus_update, edificio_detail, espaco_detail, campus_detail, componentes, componente_delete, \
    componente_detail, componente_update, recurso_update, equipamento_update, servico_update, empresa_update, \
    edificio_update, \
    espaco_update, universidade_update, recurso_atribuir, recurso_atribuir_list, recurso_atribuir_cancelar \
    , recurso_ajax, recurso_ajax_detail, recursosv1

app_name = 'Recurso'

urlpatterns = [

    # RECURSO
    path('', recursos, name='recursos'),
    path('all/<int:my_id>/<str:tipo>/<int:log>', recursosv2, name='recursos-2'),
    path('all/<int:my_id>', recursosv1, name='recursos-1'),
    path('atribuir/<int:my_id>/<str:tipo>/<int:time>/<int:log>', recurso_atribuir_list, name='recurso-atribuir-list'),
    path('atribuir-2/<int:my_id>/<int:obj_id>/<int:time>/<int:log>', recurso_atribuir, name='recurso-atribuir'),
    path('atribuir-cancelar/<int:my_id>/<int:obj_id>/<int:log>/<str:tipo>', recurso_atribuir_cancelar,
         name='recurso-atribuir-cancelar'),
    path('recurso/<int:my_id>/detail/', recurso_detail, name='recurso-detail'),
    path('recurso/<int:my_id>/delete/', recurso_delete, name='recurso-delete'),
    path('recurso/<int:my_id>/', recurso_update, name='recurso-update'),

    # COMPONENTE
    path('componentes', componentes, name='componentes'),
    path('componentes/<int:my_id>/delete/', componente_delete, name='componente-delete'),
    path('componente/<int:my_id>/detail', componente_detail, name='componente-detail'),
    path('componente/<int:my_id>/', componente_update, name='componente-update'),

    # ESPAÇO
    # path('espaco', espacos, name='espacos'),
    path('espaco/espaco_create/', espaco_create, name='espaco-create'),
    path('espaco/<int:my_id>/delete/', espaco_delete, name='espaco-delete'),
    path('espaco/<int:my_id>/detail/', espaco_detail, name='espaco-detail'),
    path('espaco/<int:my_id>/', espaco_update, name='espaco-update'),

    # EQUIPAMENTOS
    # path('equip', equipamentos, name='equipamentos'),
    path('equip/equipamento_create/', equipamento_create, name='equipamento-create'),
    path('equip/<int:my_id>/delete/', equipamento_delete, name='equipamento-delete'),
    path('equip/<int:my_id>/detail/', equipamento_detail, name='equipamento-detail'),
    path('equip/<int:my_id>/', equipamento_update, name='equipamento-update'),

    # SERVIÇOS
    # path('servico', servicos, name='servicos'),
    path('servico/servico_create/', servico_create, name='servico-create'),
    path('servico/<int:my_id>/delete/', servico_delete, name='servico-delete'),
    path('servico/<int:my_id>/detail/', servico_detail, name='servico-detail'),
    path('servico/<int:my_id>/', servico_update, name='servico-update'),

    # EMPRESAS
    # path('empresa', empresas, name='empresas'),
    path('empresa/empresa_create/', empresa_create, name='empresa-create'),
    path('empresa/<int:my_id>/delete/', empresa_delete, name='empresa-delete'),
    path('empresa/<int:my_id>/detail/', empresa_detail, name='empresa-detail'),
    path('empresa/<int:my_id>/', empresa_update, name='empresa-update'),

    # EDIFICIOS
    # path('edificio', edificios, name='edificios'),
    path('edificio/edificio_create/', edificio_create, name='edificio-create'),
    path('edificio/<int:my_id>/delete/', edificio_delete, name='edificio-delete'),
    path('edificio/<int:my_id>/detail/', edificio_detail, name='edificio-detail'),
    path('edificio/<int:my_id>/', edificio_update, name='edificio-update'),

    # UNIDADE ORGANICA
    # path('unidade-organica', unidadesorganicas, name='unidades-organicas'),
    path('unidade-organica/unidade-organica_create/', unidadeorganica_create, name='unidade-organica-create'),
    path('unidade-organica/<int:my_id>/delete/', unidadeorganica_delete, name='unidade-organica-delete'),
    path('unidade-organica/<int:my_id>/detail/', unidadeorganica_detail, name='unidade-organica-detail'),
    path('unidade-organica/<int:my_id>/', unidadeorganica_update, name='unidade-organica-update'),

    # UNIVERSIDADE
    # path('universidade', universidades, name='universidades'),
    path('universidade/universidade_create/', universidade_create, name='universidade-create'),
    path('universidade/<int:my_id>/delete/', universidade_delete, name='universidade-delete'),
    path('universidade/<int:my_id>/detail/', universidade_detail, name='universidade-detail'),
    path('universidade/<int:my_id>/', universidade_update, name='universidade-update'),

    # CAMPUS
    # path('campus', campis, name='campis'),
    path('campus/campus_create/', campus_create, name='campus-create'),
    path('campus/<int:my_id>/delete/', campus_delete, name='campus-delete'),
    path('campus/<int:my_id>/detail/', campus_detail, name='campus-detail'),
    path('campus/<int:my_id>/', campus_update, name='campus-update'),

    # AJAX
    path('ajax/', recurso_ajax, name='recurso-ajax'),
    path('ajax_detail/', recurso_ajax_detail, name='recurso-ajax-detail'),
]

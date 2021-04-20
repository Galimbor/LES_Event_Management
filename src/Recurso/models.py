from django.db import models

# Create your models here.
from Evento.models import Logistica, Evento
from Neglected.models import Timedate
from Utilizadores.models import Servicostecnicos


class Unidadeorganica(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255)  # Field name made lowercase.
    universidadeid = models.ForeignKey('Universidade', models.DO_NOTHING,
                                       db_column='UniversidadeID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'UnidadeOrganica'


class Universidade(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255)  # Field name made lowercase.
    localizacao = models.CharField(db_column='Localizacao', max_length=255, blank=True,
                                   null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Universidade'


class Empresa(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255)  # Field name made lowercase.
    descricao = models.CharField(db_column='Descricao', max_length=255, blank=True,
                                 null=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=255)  # Field name made lowercase.
    telefone = models.CharField(db_column='Telefone', max_length=255, blank=True,
                                null=True)  # Field name made lowercase.
    cidade = models.CharField(db_column='Cidade', max_length=255)  # Field name made lowercase.
    endereco = models.CharField(db_column='Endereço', max_length=255)  # Field name made lowercase.
    codigopostal = models.CharField(db_column='CodigoPostal', max_length=255)  # Field name made lowercase.
    faturacao = models.CharField(db_column='Faturacao', max_length=255, blank=True,
                                 null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Empresa'


class Recurso(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255)  # Field name made lowercase.
    fonte = models.CharField(db_column='Fonte', max_length=255)  # Field name made lowercase.
    empresaid = models.ForeignKey(Empresa, models.DO_NOTHING, db_column='EmpresaID', blank=True,
                                  null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Recurso'


class Servico(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255)  # Field name made lowercase.
    reservada = models.TextField(db_column='Reservada')  # Field name made lowercase. This field type is a guess.
    recursoid = models.ForeignKey(Recurso, models.DO_NOTHING, db_column='RecursoID')  # Field name made lowercase.
    unidadeorganicaid = models.ForeignKey('Unidadeorganica', models.DO_NOTHING, db_column='UnidadeOrganicaID',
                                          blank=True, null=True)  # Field name made lowercase.
    tiposervicoid = models.IntegerField(db_column='TipoServicoid')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Servico'


class Espaco(models.Model):
    capacidade = models.IntegerField(db_column='Capacidade')  # Field name made lowercase.
    mobilidade = models.IntegerField(db_column='Mobilidade')  # Field name made lowercase.
    recursoid = models.ForeignKey('Recurso', models.DO_NOTHING, db_column='RecursoID')  # Field name made lowercase.
    tipoespacoid = models.IntegerField(db_column='TipoEspacoid')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Espaco'


class EventoRecurso(models.Model):
    eventoid = models.OneToOneField(Evento, models.DO_NOTHING, db_column='EventoID')  # Field name made lowercase.
    recursoid = models.OneToOneField('Recurso', models.DO_NOTHING, db_column='RecursoID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Evento_Recurso'


class Campus(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255)  # Field name made lowercase.
    localizacao = models.CharField(db_column='Localizaçao', max_length=255, blank=True,
                                   null=True)  # Field name made lowercase.
    universidadeid = models.ForeignKey('Universidade', models.DO_NOTHING,
                                       db_column='UniversidadeID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Campus'


class Edificio(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255)  # Field name made lowercase.
    localizacao = models.CharField(db_column='Localizaçao', max_length=255, blank=True,
                                   null=True)  # Field name made lowercase.
    campusid = models.ForeignKey(Campus, models.DO_NOTHING, db_column='CampusID', blank=True,
                                 null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Edificio'


class Sala(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.IntegerField(db_column='Nome')  # Field name made lowercase.
    espacoid = models.ForeignKey(Espaco, models.DO_NOTHING, db_column='Espacoid')  # Field name made lowercase.
    edificioid = models.ForeignKey(Edificio, models.DO_NOTHING, db_column='EdificioID', blank=True,
                                   null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Sala'


class Equipamento(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', unique=True, max_length=255)  # Field name made lowercase.
    descricao = models.CharField(db_column='Descricao', max_length=255, blank=True,
                                 null=True)  # Field name made lowercase.
    reservado = models.IntegerField(db_column='Reservado', blank=True, null=True)  # Field name made lowercase.
    recursoid = models.ForeignKey('Recurso', models.DO_NOTHING,
                                  db_column='RecursoID')  # Field name made lowercase.
    unidadeorganicaid = models.ForeignKey('Unidadeorganica', models.DO_NOTHING,
                                          db_column='UnidadeOrganicaID')  # Field name made lowercase.
    espacoid = models.ForeignKey('Espaco', models.DO_NOTHING, db_column='Espacoid', blank=True,
                                 null=True)  # Field name made lowercase.
    tipodeequipamentoid = models.IntegerField(db_column='TipodeEquipamentoID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Equipamento'


class Tipoespaco(models.Model):
    nome = models.IntegerField(unique=True)
    quantidade = models.IntegerField(blank=True, null=True)
    logisticaid = models.ForeignKey(Logistica, models.DO_NOTHING, db_column='Logisticaid')  # Field name made lowercase.
    horariorequisicao = models.ForeignKey(Timedate, models.DO_NOTHING,
                                          db_column='HorarioRequisicao')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TipoEspaco'


class Tiposervico(models.Model):
    nome = models.IntegerField(unique=True)
    quantidade = models.IntegerField(blank=True, null=True)
    logisticaid = models.ForeignKey(Logistica, models.DO_NOTHING, db_column='Logisticaid')  # Field name made lowercase.
    horariorequisicao = models.ForeignKey(Timedate, models.DO_NOTHING,
                                          db_column='HorarioRequisicao')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TipoServico'


class Tipodeequipamento(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.IntegerField(unique=True)
    quantidade = models.IntegerField(blank=True, null=True)
    logisticaid = models.ForeignKey(Logistica, models.DO_NOTHING, db_column='Logisticaid')  # Field name made lowercase.
    horariorequisicao = models.ForeignKey(Timedate, models.DO_NOTHING,
                                          db_column='HorarioRequisicao')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TipodeEquipamento'

from django.db import models

# Create your models here.
from Evento.models import Logistica, Evento
from Neglected.models import Timedate
from Utilizadores.models import Servicostecnicos


class Unidadeorganica(models.Model):
    def __str__(self):
        return self.nome

    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255)  # Field name made lowercase.
    universidadeid = models.ForeignKey('Universidade', models.DO_NOTHING,
                                       db_column='UniversidadeID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'UnidadeOrganica'


class Universidade(models.Model):
    def __str__(self):
        return self.nome

    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255)  # Field name made lowercase.
    localizacao = models.CharField(db_column='Localizacao', max_length=255, blank=True,
                                   null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Universidade'


class Empresa(models.Model):
    def __str__(self):
        return self.nome

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


class Servico(models.Model):
    def __str__(self):
        return self.nome

    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255)  # Field name made lowercase.
    descricao = models.CharField(db_column='Descricao', max_length=255)
    unidadeorganicaid = models.ForeignKey('Unidadeorganica', models.DO_NOTHING, db_column='UnidadeOrganicaID',
                                          blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Servico'


class EventoRecurso(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    eventoid = models.OneToOneField(Evento, models.DO_NOTHING, db_column='EventoID')  # Field name made lowercase.
    recursoid = models.OneToOneField('Recurso', models.DO_NOTHING, db_column='RecursoID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Evento_Recurso'


class Campus(models.Model):
    def __str__(self):
        return self.nome

    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255)  # Field name made lowercase.
    # localizacao = models.CharField(db_column='Localizaçao', max_length=255, blank=True,
    #                                null=True)  # Field name made lowercase.
    universidadeid = models.ForeignKey('Universidade', models.DO_NOTHING,
                                       db_column='UniversidadeID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Campus'


class Edificio(models.Model):
    def __str__(self):
        return self.nome

    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255)  # Field name made lowercase.
    localizacao = models.CharField(db_column='Localizaçao', max_length=255, blank=True,
                                   null=True)  # Field name made lowercase.
    campusid = models.ForeignKey(Campus, models.DO_NOTHING, db_column='CampusID', blank=True,
                                 null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Edificio'


class Espaco(models.Model):
    def __str__(self):
        return self.nome

    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255)
    tipo = models.CharField(db_column='Tipo', max_length=255)
    capacidade = models.IntegerField(db_column='Capacidade')  # Field name made lowercase.
    mobilidade = models.BooleanField(db_column='Mobilidade')  # Field name made lowercase.
    edificioid = models.ForeignKey('Edificio', models.DO_NOTHING, db_column='EdificioID', blank=True,
                                   null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Espaco'


class Equipamento(models.Model):
    def __str__(self):
        return self.nome

    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', unique=True, max_length=255)  # Field name made lowercase.
    descricao = models.CharField(db_column='Descricao', max_length=255)  # Field name made lowercase.
    unidadeorganicaid = models.ForeignKey('Unidadeorganica', models.DO_NOTHING,
                                          db_column='UnidadeOrganicaID', blank=True,
                                          null=True)  # Field name made lowercase.
    espacoid = models.ForeignKey('Espaco', models.DO_NOTHING, db_column='Espacoid', blank=True,
                                 null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Equipamento'


class Recurso(models.Model):
    def __str__(self):
        return self.nome

    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255)  # Field name made lowercase.
    fonte = models.CharField(db_column='Fonte', max_length=255)  # Field name made lowercase.
    empresaid = models.ForeignKey(Empresa, models.DO_NOTHING, db_column='EmpresaID', blank=True,
                                  null=True)  # Field name made lowercase.
    espacoid = models.ForeignKey(Espaco, models.DO_NOTHING, db_column='EspacoId', blank=True, null=True)
    servicoid = models.ForeignKey(Servico, models.DO_NOTHING, db_column='ServicoId', blank=True, null=True)
    equipamentoid = models.ForeignKey(Equipamento, models.DO_NOTHING, db_column='EquipamentoId', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Recurso'


class Tipoespaco(models.Model):
    def __str__(self):
        return self.nome

    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(unique=True, max_length=255)
    quantidade = models.IntegerField(blank=True, null=True)
    logisticaid = models.ForeignKey(Logistica, models.DO_NOTHING, db_column='Logisticaid')  # Field name made lowercase.
    horariorequisicao = models.ForeignKey(Timedate, models.DO_NOTHING,
                                          db_column='HorarioRequisicao')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TipoEspaco'


class Tiposervico(models.Model):
    def __str__(self):
        return self.nome

    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(unique=True, max_length=255)
    quantidade = models.IntegerField(blank=True, null=True)
    logisticaid = models.ForeignKey(Logistica, models.DO_NOTHING, db_column='Logisticaid')  # Field name made lowercase.
    horariorequisicao = models.ForeignKey(Timedate, models.DO_NOTHING,
                                          db_column='HorarioRequisicao')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TipoServico'


class Tipodeequipamento(models.Model):
    def __str__(self):
        return self.nome

    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(unique=True, max_length=255)
    quantidade = models.IntegerField(blank=True, null=True)
    logisticaid = models.ForeignKey(Logistica, models.DO_NOTHING, db_column='Logisticaid')  # Field name made lowercase.
    horariorequisicao = models.ForeignKey(Timedate, models.DO_NOTHING,
                                          db_column='HorarioRequisicao')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TipodeEquipamento'


class TimedateRecurso(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    timedateid = models.OneToOneField(Timedate, models.DO_NOTHING, db_column='TimeDateID')  # Field name made lowercase.
    recursoid = models.OneToOneField(Recurso, models.DO_NOTHING, db_column='RecursoID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TimeDate_Recurso'
        unique_together = (('timedateid', 'recursoid'),)

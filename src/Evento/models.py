from django.db import models

# Create your models here.
from Neglected.models import Timedate
from Utilizadores.models import ProponenteInterno, ProponenteExterno


class Tipoevento(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TipoEvento'


class Templatecertificado(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    destinatario = models.CharField(db_column='Destinatario', max_length=255)  # Field name made lowercase.
    dataemissao = models.CharField(db_column='DataEmissao', max_length=255)  # Field name made lowercase.
    formularioid = models.IntegerField(db_column='FormularioId')  # Field name made lowercase.
    eventoid = models.IntegerField(db_column='EventoID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TemplateCertificado'


class Evento(models.Model):
    def _str_(self):
        return self.nome
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255)  # Field name made lowercase.
    descricaogeral = models.TextField(db_column='DescricaoGeral')  # Field name made lowercase.
    maxparticipantes = models.IntegerField(db_column='MaxParticipantes')  # Field name made lowercase.
    estado = models.CharField(db_column='Estado', max_length=255, blank=True, null=True)  # Field name made lowercase.
    visibilidade = models.CharField(db_column='Visibilidade', max_length=255, blank=True,
                                    null=True, default='Público')  # Field name made lowercase.
    tipoeventoid = models.ForeignKey(Tipoevento, models.DO_NOTHING, db_column='TipoEventoID', blank=True,
                                     null=True)  # Field name made lowercase.
    certificadoid = models.ForeignKey(Templatecertificado, models.DO_NOTHING,
                                      db_column='CertificadoID', blank=True,
                                     null=True)  # Field name made lowercase.
    proponente_internoid = models.ForeignKey(ProponenteInterno, models.DO_NOTHING,
                                             db_column='Proponente internoID', blank=True,
                                     null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    proponente_externoid = models.ForeignKey(ProponenteExterno, models.DO_NOTHING,
                                             db_column='Proponente ExternoID', blank=True,
                                     null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    horario = models.ForeignKey(Timedate, models.DO_NOTHING, db_column='Horario')  # Field name made lowercase.
    inscritos = models.IntegerField(db_column='Num_participantes')
    val_inscritos = models.IntegerField(db_column='Validacao_inscritos')

    class Meta:
        managed = False
        db_table = 'Evento'






class Logistica(models.Model):
    def _str_(self):
        return self.nome
    id = models.AutoField(db_column='ID', primary_key=True)  # Id
    nome = models.CharField(db_column='Nome', max_length=255)  # Field name made lowercase.
    eventoid = models.ForeignKey(Evento, models.DO_NOTHING, db_column='EventoID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Logistica'

    def __str__(self):
        return self.nome
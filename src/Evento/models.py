from django.db import models

# Create your models here.


from GestorTemplates.models import Templatecertificado, Tipoevento
from Neglected.models import Timedate
from Utilizadores.models import ProponenteInterno, ProponenteExterno


class Evento(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255)  # Field name made lowercase.
    descricaogeral = models.CharField(db_column='DescricaoGeral', max_length=255)  # Field name made lowercase.
    maxparticipantes = models.IntegerField(db_column='MaxParticipantes')  # Field name made lowercase.
    estado = models.CharField(db_column='Estado', max_length=255, blank=True, null=True)  # Field name made lowercase.
    visibilidade = models.CharField(db_column='Visibilidade', max_length=255, blank=True,
                                    null=True)  # Field name made lowercase.
    tipoeventoid = models.ForeignKey(Tipoevento, models.DO_NOTHING, db_column='TipoEventoID', blank=True,
                                     null=True)  # Field name made lowercase.
    certificadoid = models.ForeignKey(Templatecertificado, models.DO_NOTHING,
                                      db_column='CertificadoID')  # Field name made lowercase.
    proponente_internoid = models.ForeignKey(ProponenteInterno, models.DO_NOTHING,
                                             db_column='Proponente internoID')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    proponente_externoid = models.ForeignKey(ProponenteExterno, models.DO_NOTHING,
                                             db_column='Proponente ExternoID')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    horario = models.ForeignKey(Timedate, models.DO_NOTHING, db_column='Horario')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Evento'


class Feedback(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    descricao = models.CharField(db_column='Descricao', max_length=255, blank=True,
                                 null=True)  # Field name made lowercase.
    eventoid = models.ForeignKey(Evento, models.DO_NOTHING, db_column='EventoID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Feedback'


class Logistica(models.Model):
    nome = models.IntegerField(db_column='Nome', blank=True, null=True)  # Field name made lowercase.
    eventoid = models.ForeignKey(Evento, models.DO_NOTHING, db_column='EventoID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Logistica'

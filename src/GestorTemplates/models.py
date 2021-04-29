from django.db import models

# Create your models here.
# from Evento.models import Feedback, Evento
from Evento.models import Evento, Tipoevento
from Inscricao.models import Inscricao
from Utilizadores.models import Gcp
from Feedback.models import Feedback


class Campo(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    conteudo = models.CharField(db_column='Conteudo', max_length=255)  # Field name made lowercase.
    obrigatorio = models.BooleanField(db_column='Obrigatorio')  # Field name made lowercase. This field type is a guess.
    tipocampoid = models.ForeignKey('Tipocampo', models.DO_NOTHING,
                                    db_column='TipoCampoID')  # Field name made lowercase.
    respostapossivelid = models.ForeignKey('Respostaspossiveis', models.DO_NOTHING, db_column='RespostaPossivelId',
                                           blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Campo'


class CampoFormulario(models.Model):
    campoid = models.ForeignKey(Campo, models.DO_NOTHING, db_column='CampoID')  # Field name made lowercase.
    formularioid = models.ForeignKey('Formulario', models.DO_NOTHING,
                                     db_column='FormularioId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Campo_Formulario'


class Formulario(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    visibilidade = models.CharField(db_column='Visibilidade', max_length=255)  # Field name made lowercase.
    tipoeventoid = models.ForeignKey(Tipoevento, models.DO_NOTHING,
                                     db_column='TipoEventoID')  # Field name made lowercase.
    tipoformularioid = models.ForeignKey('Tipoformulario', models.DO_NOTHING,
                                         db_column='TipoFormularioID')  # Field name made lowercase.
    gcpid = models.ForeignKey(Gcp, models.DO_NOTHING, db_column='GCPid')  # Field name made lowercase.

    eventoid = models.ForeignKey(Evento, models.DO_NOTHING, db_column='eventoID')

    class Meta:
        managed = False
        db_table = 'Formulario'


class GcpFormulario(models.Model):
    gcpid = models.OneToOneField(Gcp, models.DO_NOTHING, db_column='GCPid',
                                 primary_key=True)  # Field name made lowercase.
    formularioid = models.ForeignKey(Formulario, models.DO_NOTHING,
                                     db_column='FormularioId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'GCP_Formulario'
        unique_together = (('gcpid', 'formularioid'),)


class Resposta(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    conteudo = models.CharField(db_column='Conteudo', max_length=255)  # Field name made lowercase.
    campoid = models.ForeignKey(Campo, models.DO_NOTHING, db_column='CampoID', blank=True,
                                null=True)  # Field name made lowercase.
    feedbackid = models.ForeignKey(Feedback, models.DO_NOTHING, db_column='FeedbackId', blank=True,
                                   null=True)  # Field name made lowercase.
    inscricaoid = models.ForeignKey(Inscricao, models.DO_NOTHING, db_column='InscricaoId', blank=True,
                                    null=True)  # Field name made lowercase.
    eventoid = models.ForeignKey(Evento, models.DO_NOTHING, db_column='EventoID', blank=True,
                                 null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Resposta'


class Tipocampo(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TipoCampo'


class Tipoformulario(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TipoFormulario'


class Respostaspossiveis(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'RespostasPossiveis'
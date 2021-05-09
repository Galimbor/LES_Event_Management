from django.db import models

# Create your models here.
# from Evento.models import Feedback, Evento
from Evento.models import Evento, Tipoevento
from Inscricao.models import Inscricao
from Utilizadores.models import Gcp
from Feedback.models import Feedback

caterogias_tipo_formulario = [
    ("0", "Evento"),
    ("1", "Inscrição"),
    ("2", "Feedback"),
]

''' Assumo que Tipoformulario funciona como subtipo de evento
ex.: Seminario (nome do tipoFormulario) é Tipoformulario, categoria = evento
    inscriçao é TipoFormulario, categoria = inscrição
'''
class Tipoformulario(models.Model):
    id = models.AutoField(
        db_column="ID", primary_key=True
    )  # Field name made lowercase.
    nome = models.CharField(
        db_column="Nome", max_length=255
    )  # Field name made lowercase.
    categoria = models.CharField(
        db_column="Categoria",
        max_length=255,
        choices= caterogias_tipo_formulario,
        default="0",
    )

    class Meta:
        managed = False
        db_table = "TipoFormulario"

    def __str__(self):
        return '{}-{}' .format(self.get_categoria_display(), self.nome)


class Formulario(models.Model):
    id = models.AutoField(
        db_column="Id", primary_key=True
    )  # Field name made lowercase.
    nome = models.CharField(db_column="Nome", max_length=255, default="Sem título")
    VISIBILIDADE = [
        ("0", "Público"),
        ("1", "Privado"),
    ]
    visibilidade = models.CharField(
        db_column="Visibilidade", max_length=255, choices=VISIBILIDADE, default="0"
    )
    is_template = models.IntegerField(
        db_column="IsTemplate",
        choices=[
            (0, "Não"),
            (1, "Sim"),
        ],
        default=0,
        verbose_name="É Template?",
    )
    tipoeventoid = models.ForeignKey(
        Tipoevento, models.DO_NOTHING, db_column="TipoEventoID", null=True
    )  
    tipoformularioid = models.ForeignKey(
        "Tipoformulario", models.DO_NOTHING, db_column="TipoFormularioID", null=True
    )  # Field name made lowercase.
    gcpid = models.ForeignKey(
        Gcp, models.DO_NOTHING, db_column="GCPid"
    )  # Field name made lowercase.

    eventoid = models.ForeignKey(Evento, models.DO_NOTHING, db_column="eventoID")

    class Meta:
        managed = False
        db_table = "Formulario"

    def __str__(self):
        return self.nome


class Campo(models.Model):
    id = models.AutoField(
        db_column="ID", primary_key=True
    )  # Field name made lowercase.
    conteudo = models.CharField(
        db_column="Conteudo", max_length=255
    )  # Field name made lowercase.
    obrigatorio = models.BooleanField(
        db_column="Obrigatorio"
    )  # Field name made lowercase. This field type is a guess.
    tipocampoid = models.ForeignKey(
        "Tipocampo", models.DO_NOTHING, db_column="TipoCampoID"
    )  # Field name made lowercase.
    respostapossivelid = models.ForeignKey(
        "Respostaspossiveis",
        models.DO_NOTHING,
        db_column="RespostaPossivelId",
        blank=True,
        null=True,
    )  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = "Campo"

    def __str__(self):
        return self.conteudo


class CampoFormulario(models.Model):
    campoid = models.ForeignKey(
        Campo, models.DO_NOTHING, db_column="CampoID"
    )  # Field name made lowercase.
    formularioid = models.ForeignKey(
        "Formulario", models.DO_NOTHING, db_column="FormularioId"
    )  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = "Campo_Formulario"


class GcpFormulario(models.Model):
    gcpid = models.OneToOneField(
        Gcp, models.DO_NOTHING, db_column="GCPid", primary_key=True
    )  # Field name made lowercase.
    formularioid = models.ForeignKey(
        Formulario, models.DO_NOTHING, db_column="FormularioId"
    )  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = "GCP_Formulario"
        unique_together = (("gcpid", "formularioid"),)


class Resposta(models.Model):
    id = models.AutoField(
        db_column="ID", primary_key=True
    )  # Field name made lowercase.
    conteudo = models.CharField(
        db_column="Conteudo", max_length=255
    )  # Field name made lowercase.
    campoid = models.ForeignKey(
        Campo, models.DO_NOTHING, db_column="CampoID", blank=True, null=True
    )  # Field name made lowercase.
    feedbackid = models.ForeignKey(
        Feedback, models.DO_NOTHING, db_column="FeedbackId", blank=True, null=True
    )  # Field name made lowercase.
    inscricaoid = models.ForeignKey(
        Inscricao, models.DO_NOTHING, db_column="InscricaoId", blank=True, null=True
    )  # Field name made lowercase.
    eventoid = models.ForeignKey(
        Evento, models.DO_NOTHING, db_column="EventoID", blank=True, null=True
    )  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = "Resposta"


class Tipocampo(models.Model):
    id = models.AutoField(
        db_column="ID", primary_key=True
    )  # Field name made lowercase.
    nome = models.CharField(
        db_column="Nome", max_length=255
    )  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = "TipoCampo"


class Respostaspossiveis(models.Model):
    id = models.AutoField(
        db_column="Id", primary_key=True
    )  # Field name made lowercase.
    nome = models.CharField(
        db_column="Nome", max_length=255
    )  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = "RespostasPossiveis"

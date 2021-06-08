from django.db import models
from django.utils import timezone

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

""" Assumo que Tipoformulario funciona como subtipo de evento
ex.: Seminario (nome do tipoFormulario) é Tipoformulario, categoria = evento
    inscriçao é TipoFormulario, categoria = inscrição
"""
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
        choices=caterogias_tipo_formulario,
        default="0",
    )

    class Meta:
        managed = True
        db_table = "TipoFormulario"

    def __str__(self):
        return self.nome


class Formulario(models.Model):
    id = models.AutoField(
        db_column="Id", primary_key=True
    )  # Field name made lowercase.
    nome = models.CharField(db_column="Nome", max_length=255, default="Sem título")
    VISIBILIDADE_list = [
        ("0", "Privado"),
        ("1", "Utilizadores da aplicação"),
        ("2", "Público"),
    ]
    visibilidade = models.CharField(
        db_column="Visibilidade", max_length=255, choices=VISIBILIDADE_list, default="0"
    )
    TEMPLATE_LIST = [
            (0, "Não"),
            (1, "Sim"),
    ]
    is_template = models.IntegerField(
        db_column="IsTemplate",
        choices=TEMPLATE_LIST,
        default=0,
        verbose_name="É Template?",
    )
    created = models.DateTimeField(db_column="DataCriado", default = timezone.now)
    updated = models.DateTimeField(db_column="DataAtualizado", null=True, blank=True)
    tipoeventoid = models.ForeignKey(
        Tipoevento, models.DO_NOTHING, db_column="TipoEventoID", null=True
    )
    tipoformularioid = models.ForeignKey(
        "Tipoformulario", models.DO_NOTHING, db_column="TipoFormularioID", null=True
    )  # Field name made lowercase.
    gcpid = models.ForeignKey(
        Gcp, models.DO_NOTHING, db_column="GCPid"
    )  # Field name made lowercase.

    # eventoid = models.ForeignKey(Evento, models.DO_NOTHING, db_column="eventoID")
  

    class Meta:
        managed = True
        db_table = "Formulario"

    def __str__(self):
        return self.nome


class Tipocampo(models.Model):
    id = models.AutoField(
        db_column="ID", primary_key=True
    )  # Field name made lowercase.
    nome = models.CharField(
        db_column="Nome", max_length=255
    )  # Field name made lowercase.
    template = models.TextField(
        db_column="Template", default='', blank=True
    )

       
    def __str__(self):
        return self.nome


    class Meta:
        managed = True
        db_table = "TipoCampo"


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
        "Tipocampo", models.CASCADE, db_column="TipoCampoID"
    )  # Field name made lowercase.
    campo_relacionado = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)
    position_index = models.IntegerField(default = 0,  db_column="Posicao")
    respostapossivelid = models.ForeignKey(
        "Respostaspossiveis",
        models.DO_NOTHING,
        db_column="RespostaPossivelId",
        blank=True,
        null=True,
    )  # Field name made lowercase.


    class Meta:
        managed = True
        db_table = "Campo"

    def __str__(self):
        return self.conteudo


class CampoFormulario(models.Model):
    campoid = models.ForeignKey(
        Campo, models.CASCADE, db_column="CampoID"
    )  # Field name made lowercase.
    formularioid = models.ForeignKey(
        "Formulario", models.CASCADE, db_column="FormularioId"
    )  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = "Campo_Formulario"
    
    def __str__(self):
        return "Form: {} ---- Pergunta: {}".format(self.formularioid,self.campoid)





class Resposta(models.Model):
    id = models.AutoField(
        db_column="ID", primary_key=True
    )  # Field name made lowercase.
    conteudo = models.CharField(
        db_column="Conteudo", max_length=255
    )  # Field name made lowercase.
    campoid = models.ForeignKey(
        Campo, models.SET_NULL, db_column="CampoID", blank=True, null=True
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
        managed = True
        db_table = "Resposta"
    
    def __str__(self):
        return self.conteudo



class Respostaspossiveis(models.Model):
    id = models.AutoField(
        db_column="Id", primary_key=True
    )  # Field name made lowercase.
    nome = models.CharField(
        db_column="Nome", max_length=255
    )  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = "RespostasPossiveis"



class GcpFormulario(models.Model):
    gcpid = models.OneToOneField(
        Gcp, models.DO_NOTHING, db_column="GCPid", primary_key=True
    )  # Field name made lowercase.
    formularioid = models.ForeignKey(
        Formulario, models.DO_NOTHING, db_column="FormularioId"
    )  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = "GCP_Formulario"
        unique_together = (("gcpid", "formularioid"),)
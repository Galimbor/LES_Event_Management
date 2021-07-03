from django.db import models

# Create your models here.
from Evento.models import Evento
from GestorTemplates.models import Formulario


class EventoFormulario(models.Model):
    eventoid = models.ForeignKey(
        Evento, models.CASCADE, db_column="eventoID"
    )  # Field name made lowercase.
    formularioid = models.ForeignKey(
        Formulario, models.CASCADE, db_column="formularioID"
    )  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = "Evento_Formulario"

    def __str__(self):
        return "Evento: {} ---- Formulario: {}".format( self.eventoid, self.formularioid)



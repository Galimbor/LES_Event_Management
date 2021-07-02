from django.db import models

from Evento.models import Evento
from Utilizadores.models import User

class Feedback(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    descricao = models.CharField(db_column='Descricao', max_length=255, blank=True,
                                 null=True)  # Field name made lowercase.
    eventoid = models.ForeignKey(Evento, models.DO_NOTHING, db_column='EventoID')  # Field name made lowercase.

    userid = models.ForeignKey(User, models.DO_NOTHING, db_column='UserID')

    createdAt = models.DateTimeField(db_column='createdAt')

    class Meta:
        managed = False
        db_table = 'Feedback'
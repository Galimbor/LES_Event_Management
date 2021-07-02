from django.db import models

# Create your models here.

class Timedate(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    datainicial = models.DateField(db_column='DataInicial')  # Field name made lowercase.
    horainicial = models.TimeField(db_column='HoraInicial')  # Field name made lowercase.
    datafinal = models.DateField(db_column='DataFinal', blank=True, null=True)  # Field name made lowercase.
    horafinal = models.TimeField(db_column='HoraFinal', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TimeDate'


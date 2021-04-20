from django.db import models


# Create your models here.


class Admin(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    gabinete = models.CharField(db_column='Gabinete', max_length=255, blank=True,
                                null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Admin'


class Gcp(models.Model):
    class Meta:
        managed = False
        db_table = 'GCP'


class ProponenteExterno(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    profissao = models.CharField(max_length=255, blank=True, null=True)
    empresa = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Proponente Externo'


class ProponenteInterno(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    numeroualg = models.IntegerField(db_column='numeroUALG', blank=True, null=True)  # Field name made lowercase.
    curso = models.CharField(max_length=255, blank=True, null=True)
    profissao = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Proponente interno'


class Servicostecnicos(models.Model):
    class Meta:
        managed = False
        db_table = 'ServicosTecnicos'


class User(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=255, blank=True,
                                null=True)  # Field name made lowercase.
    last_login = models.DateTimeField(db_column='Last_login', blank=True, null=True)  # Field name made lowercase.
    is_superuser = models.IntegerField(blank=True, null=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.IntegerField(blank=True, null=True)
    date_joined = models.DateTimeField(blank=True, null=True)
    morada = models.CharField(max_length=255, blank=True, null=True)
    contribuinte = models.IntegerField(blank=True, null=True)
    datanascimento = models.DateTimeField(db_column='dataNascimento', blank=True,
                                          null=True)  # Field name made lowercase.
    adminid = models.ForeignKey(Admin, models.DO_NOTHING, db_column='AdminId', blank=True,
                                null=True)  # Field name made lowercase.
    gcpid = models.ForeignKey(Gcp, models.DO_NOTHING, db_column='GCPid', blank=True,
                              null=True)  # Field name made lowercase.
    proponente_externoid = models.ForeignKey(ProponenteExterno, models.DO_NOTHING,
                                             db_column='Proponente Externoid', blank=True,
                                             null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    proponente_internoid = models.ForeignKey(ProponenteInterno, models.DO_NOTHING,
                                             db_column='Proponente internoID', blank=True,
                                             null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    servicostecnicosid = models.ForeignKey(Servicostecnicos, models.DO_NOTHING,
                                           db_column='ServicosTecnicosid', blank=True,
                                           null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'User'

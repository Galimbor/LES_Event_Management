from django.db import models


# Create your models here.


class Notificacao(models.Model):
    level = models.CharField(max_length=20)
    unread = models.IntegerField()
    actor_object_id = models.CharField(max_length=255)
    verb = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    target_object_id = models.CharField(max_length=255, blank=True, null=True)
    action_object_object_id = models.CharField(max_length=255, blank=True, null=True)
    timestamp = models.DateTimeField()
    public = models.IntegerField()
    deleted = models.IntegerField()
    emailed = models.IntegerField()
    data = models.TextField(blank=True, null=True)
    titulo = models.CharField(max_length=255)
    descricao = models.CharField(max_length=255)
    tipo = models.CharField(max_length=255)
    action_object_content_type_id = models.IntegerField(blank=True, null=True)
    actor_content_type_id = models.IntegerField()
    recipient_id = models.IntegerField()
    target_content_type_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'notificacao'


class Informacaonotificacao(models.Model):
    data = models.DateTimeField()
    pendente = models.IntegerField()
    titulo = models.CharField(max_length=255)
    descricao = models.CharField(max_length=255)
    tipo = models.CharField(max_length=255)
    lido = models.IntegerField()
    emissorid = models.IntegerField(blank=True, null=True)
    recetorid = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'informacaonotificacao'


class Mensagemenviada(models.Model):
    mensagem_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'mensagemenviada'


class Mensagemrecebida(models.Model):
    mensagem_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'mensagemrecebida'


class Informacaomensagem(models.Model):
    data = models.DateTimeField()
    pendente = models.IntegerField()
    titulo = models.CharField(max_length=255)
    descricao = models.CharField(max_length=255)
    tipo = models.CharField(max_length=255)
    lido = models.IntegerField()
    emissorid = models.IntegerField(blank=True, null=True)
    recetorid = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'informacaomensagem'

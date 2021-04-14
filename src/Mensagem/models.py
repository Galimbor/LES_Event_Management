from django.db import models

# Create your models here.



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

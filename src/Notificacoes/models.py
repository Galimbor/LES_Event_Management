from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Notificacao(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    titulo = models.CharField(max_length=255)
    descricao = models.TextField(max_length=255)

    class Estado(models.IntegerChoices):
        NOVO = 1
        LIDO = 2
        ARQUIVADO = 3

    estado = models.IntegerField(choices=Estado.choices, default=Estado.NOVO)

    tipo = models.CharField(max_length=255, default="USER")


    def __str__(self):
        return self.titulo
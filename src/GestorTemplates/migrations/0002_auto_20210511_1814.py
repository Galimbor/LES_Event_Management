# Generated by Django 3.2 on 2021-05-11 17:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('GestorTemplates', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resposta',
            name='teste',
        ),
        migrations.AddField(
            model_name='campo',
            name='campo_relacionado',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='GestorTemplates.campo'),
        ),
    ]

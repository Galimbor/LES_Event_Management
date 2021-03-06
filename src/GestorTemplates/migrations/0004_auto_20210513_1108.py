# Generated by Django 3.2 on 2021-05-13 10:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('GestorTemplates', '0003_auto_20210511_1948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campo',
            name='tipocampoid',
            field=models.ForeignKey(db_column='TipoCampoID', on_delete=django.db.models.deletion.CASCADE, to='GestorTemplates.tipocampo'),
        ),
        migrations.AlterField(
            model_name='campoformulario',
            name='campoid',
            field=models.ForeignKey(db_column='CampoID', on_delete=django.db.models.deletion.CASCADE, to='GestorTemplates.campo'),
        ),
        migrations.AlterField(
            model_name='resposta',
            name='campoid',
            field=models.ForeignKey(blank=True, db_column='CampoID', null=True, on_delete=django.db.models.deletion.SET_NULL, to='GestorTemplates.campo'),
        ),
        migrations.AlterField(
            model_name='tipocampo',
            name='template',
            field=models.TextField(blank=True, db_column='Template', default=''),
        ),
    ]

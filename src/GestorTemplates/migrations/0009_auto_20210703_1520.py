# Generated by Django 3.2 on 2021-07-03 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GestorTemplates', '0008_auto_20210604_1145'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventoFormulario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'Evento_Formulario',
                'managed': False,
            },
        ),
        migrations.AddField(
            model_name='formulario',
            name='is_arquivado',
            field=models.IntegerField(choices=[(0, 'Não'), (1, 'Sim')], db_column='IsArquivado', default=0, verbose_name='Está Arquivado ?'),
        ),
        migrations.AlterField(
            model_name='campo',
            name='conteudo',
            field=models.TextField(db_column='Conteudo'),
        ),
    ]

# Generated by Django 3.2 on 2021-05-10 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Inscricao',
            fields=[
                ('id', models.AutoField(db_column='Id', primary_key=True, serialize=False)),
                ('nome', models.CharField(db_column='Nome', max_length=255)),
                ('email', models.CharField(db_column='Email', max_length=255)),
                ('telemovel', models.IntegerField(blank=True, db_column='Telemovel', null=True)),
                ('idade', models.IntegerField(db_column='Idade')),
                ('profissao', models.CharField(blank=True, db_column='Profissao', max_length=255, null=True)),
                ('estado', models.CharField(db_column='Estado', max_length=255)),
                ('num_inscricao', models.IntegerField(db_column='Num_Inscricao')),
                ('checkin', models.BooleanField(db_column='check_in')),
            ],
            options={
                'db_table': 'Inscricao',
                'managed': False,
            },
        ),
    ]

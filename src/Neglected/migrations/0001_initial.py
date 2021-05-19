# Generated by Django 3.2 on 2021-05-18 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Timedate',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('datainicial', models.DateField(db_column='DataInicial')),
                ('horainicial', models.TimeField(db_column='HoraInicial')),
                ('datafinal', models.DateField(blank=True, db_column='DataFinal', null=True)),
                ('horafinal', models.TimeField(blank=True, db_column='HoraFinal', null=True)),
            ],
            options={
                'db_table': 'TimeDate',
                'managed': False,
            },
        ),
    ]
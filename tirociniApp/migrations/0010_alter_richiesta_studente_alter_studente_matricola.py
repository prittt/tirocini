# Generated by Django 4.0.5 on 2022-07-27 16:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tirociniApp', '0009_alter_richiesta_sede_alter_richiesta_tutor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='richiesta',
            name='studente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='tirociniApp.studente', unique=True),
        ),
        migrations.AlterField(
            model_name='studente',
            name='matricola',
            field=models.CharField(max_length=6, unique=True),
        ),
    ]

# Generated by Django 4.0.5 on 2022-07-27 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tirociniApp', '0008_sede_tutor_alter_richiesta_sede_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='richiesta',
            name='sede',
            field=models.CharField(max_length=254),
        ),
        migrations.AlterField(
            model_name='richiesta',
            name='tutor',
            field=models.CharField(max_length=60),
        ),
    ]

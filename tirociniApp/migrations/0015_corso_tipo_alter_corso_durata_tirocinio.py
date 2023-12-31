# Generated by Django 4.0.5 on 2022-10-27 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tirociniApp', '0014_corso_alter_richiesta_options_alter_sede_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='corso',
            name='tipo',
            field=models.CharField(blank=True, choices=[('LT', 'Laurea Triennale'), ('LM', 'Laurea Magistrale')], max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='corso',
            name='durata_tirocinio',
            field=models.IntegerField(default=0),
        ),
    ]

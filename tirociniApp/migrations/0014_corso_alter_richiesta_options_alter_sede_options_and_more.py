# Generated by Django 4.0.5 on 2022-10-27 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tirociniApp', '0013_alter_richiesta_stato_alter_richiesta_studente'),
    ]

    operations = [
        migrations.CreateModel(
            name='Corso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codice', models.CharField(max_length=254)),
                ('nome', models.CharField(max_length=254)),
                ('durata_tirocinio', models.IntegerField()),
            ],
            options={
                'verbose_name_plural': 'Corsi',
            },
        ),
        migrations.AlterModelOptions(
            name='richiesta',
            options={'verbose_name_plural': 'Richieste'},
        ),
        migrations.AlterModelOptions(
            name='sede',
            options={'verbose_name_plural': 'Sedi'},
        ),
        migrations.AlterModelOptions(
            name='studente',
            options={'verbose_name_plural': 'Studenti'},
        ),
        migrations.AlterModelOptions(
            name='tutor',
            options={'verbose_name_plural': 'Tutor'},
        ),
        migrations.AlterField(
            model_name='richiesta',
            name='stato',
            field=models.IntegerField(choices=[(0, 'Richiesta non ancora visionata'), (1, 'Richiesta approvata'), (-1, 'Richiesta rifiutata')], default=0),
        ),
    ]
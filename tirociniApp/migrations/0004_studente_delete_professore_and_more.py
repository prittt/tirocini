# Generated by Django 4.0.4 on 2022-06-16 14:17

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tirociniApp', '0003_alter_richiesta_autocertificazione_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Studente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=40)),
                ('cognome', models.CharField(max_length=40)),
                ('codice_fiscale', models.CharField(max_length=16)),
                ('matricola', models.CharField(max_length=6)),
                ('classe', models.CharField(choices=[('L', 'Laurea Triennale'), ('LM', 'Laurea Magistrale')], max_length=2)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.DeleteModel(
            name='Professore',
        ),
        migrations.RemoveField(
            model_name='richiesta',
            name='codice_fiscale',
        ),
        migrations.RemoveField(
            model_name='richiesta',
            name='cognome',
        ),
        migrations.RemoveField(
            model_name='richiesta',
            name='matricola',
        ),
        migrations.RemoveField(
            model_name='richiesta',
            name='nome',
        ),
        migrations.AlterField(
            model_name='richiesta',
            name='tutor',
            field=models.CharField(max_length=60),
        ),
        migrations.AddField(
            model_name='richiesta',
            name='studente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='tirociniApp.studente'),
            preserve_default=False,
        ),
    ]
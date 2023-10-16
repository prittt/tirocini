# Generated by Django 4.0.5 on 2022-07-21 11:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tirociniApp', '0005_remove_studente_cognome_remove_studente_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='richiesta',
            name='durata',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='richiesta',
            name='studente',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='tirociniApp.studente'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='studente',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]

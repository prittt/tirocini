from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import Group


class Studente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    codice_fiscale = models.CharField(max_length=16)
    matricola = models.CharField(max_length=6, unique=True)
    corso = models.ForeignKey("Corso", on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name

    class Meta:
        verbose_name_plural = "Studenti"


def get_first_and_last_name(self):
    return self.first_name + ' ' + self.last_name


User = get_user_model()
User.add_to_class("__str__", get_first_and_last_name)


class Richiesta(models.Model):
    STATI_POSSIBILI = [
        (0, 'Richiesta non ancora visionata'),
        (1, 'Richiesta approvata'),
        (-1, 'Richiesta rifiutata'),
    ]
    studente = models.ForeignKey('Studente', on_delete=models.CASCADE)
    corso = models.ForeignKey("Corso", on_delete=models.CASCADE)
    tutor = models.CharField(max_length=60)
    sede = models.CharField(max_length=254)
    durata = models.PositiveIntegerField()
    data_inizio = models.DateField('data inizio attività')
    data_fine = models.DateField('data fine attività')
    obiettivi = models.TextField()
    autocertificazione = models.BooleanField(default=False)
    stato = models.IntegerField(choices=STATI_POSSIBILI, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.studente)

    class Meta:
        verbose_name_plural = "Richieste"


class Tutor(models.Model):
    nome = models.CharField(max_length=60)
    cognome = models.CharField(max_length=60)

    def __str__(self):
        return self.nome + ' ' + self.cognome

    class Meta:
        verbose_name_plural = "Tutor"


class Sede(models.Model):
    nome = models.CharField(max_length=254)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = "Sedi"


class Corso(models.Model):
    TIPO_CHOICES = [
        ('LT', 'Laurea Triennale'),
        ('LM', 'Laurea Magistrale'),
    ]
    codice = models.CharField(max_length=254)
    nome = models.CharField(max_length=254)
    durata_tirocinio = models.IntegerField(default=0)
    tipo = models.CharField(max_length=2, choices=TIPO_CHOICES, null=True, blank=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = "Corsi"

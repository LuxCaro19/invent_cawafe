from django.db import models

class Modelo_equipo(models.Model):
    nombre = models.CharField()
    precio = models.IntegerField()
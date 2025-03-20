from django.db import models

class Procesador(models.Model):
    nombre = models.CharField()
    compania = models.CharField()
from django.db import models


class Obra(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class SalaVenta(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Ubicacion(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
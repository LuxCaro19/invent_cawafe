from django.db import models

class Ubicacion(models.Model):
    nombre = models.CharField()

    def __str__(self):
        return self.nombre

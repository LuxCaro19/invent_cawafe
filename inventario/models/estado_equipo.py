from django.db import models

  
class Estado_equipo(models.Model):
    nombre = models.CharField()

    def __str__(self):
        return self.nombre
from django.db import models

# Create your models here.

class Modelo_tipo(models.Model):
    tipo = models.CharField()

    def __str__(self):  
        return self.tipo
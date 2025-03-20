from django.db import models

class Sistema_operativo(models.Model):
    nombre = models.CharField()
    compania = models.CharField()
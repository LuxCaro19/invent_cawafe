from django.db import models

# Create your models here.

class ModeloEquipo(models.Model):
    nombre = models.CharField()
    precio = models.IntegerField()

class SistemaOperativo(models.Model):
    nombre = models.CharField()
    compania = models.CharField()

class Procesador(models.Model):
    nombre = models.CharField()
    compania = models.CharField()

class EstadoEquipo(models.Model):
    nombre = models.CharField()

class Equipos(models.Model):
    etiqueta = models.CharField()
    memoria_ram = models.IntegerField(null=True)
    almacenamiento = models.IntegerField(null=True)
    modelo = models.ForeignKey(ModeloEquipo, on_delete=models.SET_NULL, null=True )
    sistema_operativo = models.ForeignKey(SistemaOperativo, on_delete=models.SET_NULL, null=True )
    procesador = models.ForeignKey(Procesador, on_delete=models.SET_NULL, null=True )
    estado = models.ForeignKey(EstadoEquipo, on_delete=models.SET_NULL, null=True )


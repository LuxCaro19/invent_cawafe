from django.db import models

# Create your models here. 

class Modelo_marca(models.Model):
    marca = models.CharField()

    def __str__(self):  
        return self.marca
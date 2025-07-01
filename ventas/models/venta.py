from django.db import models
from django.utils import timezone
from io import BytesIO
from django.core.mail import EmailMessage
from django.db.models import CASCADE
#from reportlab.pdfgen import canvas
from inventario.models.estado_equipo import Estado_equipo
from django.conf import settings


class Venta(models.Model):
    id = models.AutoField(primary_key=True)
    fecha_venta = models.DateField(null=True)  
    id_equipo = models.ForeignKey('inventario.Equipo', on_delete=models.SET_NULL, null=True)
    id_usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    flag_aprobado_remuneraciones = models.BooleanField(default=None, null=True)  # Aprobación de remuneraciones
    flag_entregado = models.BooleanField(default=False)



    def procesar_compra(self):
        from inventario.models.equipo import Equipo  # evitar import circular

        self.fecha_venta = timezone.now()
        self.save()

        # Actualizar equipo
        equipo = self.id_equipo
        equipo.en_bodega = False
        equipo.estado_id = 7  # ID del estado 'Vendido'
        equipo.save()

        # Generar PDF
        # buffer = BytesIO()
        # p = canvas.Canvas(buffer)
        # p.drawString(100, 800, "Carta de Descuento por Planilla")
        # p.drawString(100, 780, f"Nombre: {self.nombre_receptor}")
        # p.drawString(100, 760, f"Equipo: {equipo.etiqueta}")
        # p.drawString(100, 740, f"Fecha: {self.fecha_venta}")
        # p.drawString(100, 720, f"Precio: ${equipo.modelo.precio}")
        # p.showPage()
        # p.save()
        # buffer.seek(0)
        # pdf = buffer.getvalue()

        # Enviar correo
        email = EmailMessage(
            'Compra realizada',
            'Se adjunta su carta de descuento por planilla.',
            'ventas@galilea.cl',
            ['usuario@correo.cl'],  # Cambiar en producción
        )
        #email.attach('carta_descuento.pdf', pdf, 'application/pdf')
        email.send(fail_silently=True)



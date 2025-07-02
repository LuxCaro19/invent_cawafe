import locale
from django.db import models
from django.utils import timezone
from io import BytesIO
from django.core.mail import EmailMessage
from django.conf import settings
from xhtml2pdf import pisa
from django.template.loader import render_to_string
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

class Venta(models.Model):
    id = models.AutoField(primary_key=True)
    fecha_venta = models.DateField(null=True)
    id_equipo = models.ForeignKey('inventario.Equipo', on_delete=models.SET_NULL, null=True)
    id_usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    flag_aprobado_remuneraciones = models.BooleanField(default=None, null=True)
    flag_entregado = models.BooleanField(default=False)



    def procesar_compra(self):
        from inventario.models.equipo import Equipo  # evitar import circular

        # Registrar la fecha y guardar la venta
        self.fecha_venta = timezone.now()
        self.save()

        # Actualizar equipo
        equipo = self.id_equipo
        equipo.en_bodega = False
        equipo.estado_id = 7  # Estado "Vendido"
        equipo.save()

        # Datos para el PDF
        usuario = self.id_usuario
        fecha = timezone.now().strftime('%d de %B de %Y')
        mes = timezone.now().strftime('%B del %Y')

        contexto = {
            'fecha': fecha,
            'nombre_usuario': usuario.nombre_completo,  # o el campo corre,
            'precio': equipo.modelo.precio,
            'tipo_equipo': equipo.modelo.tipo.tipo.upper(),
            'etiqueta': equipo.etiqueta,
            'mes': mes,
        }

        # Renderizar HTML y generar PDF
        html_string = render_to_string('pdf/hoja_descuento.html', contexto)
        pdf_file = BytesIO()
        pisa.CreatePDF(html_string, dest=pdf_file)
        pdf_file.seek(0)

        # Preparar y enviar correo
        email = EmailMessage(
            subject='Compra realizada – Carta de descuento',
            body='¡Felicidades! Has realizado tu compra de equipo, adjunto encontrará su carta de autorización de descuento por planilla.\n \n'\
            'Por favor dirijase al área de Remuneraciones con su hoja firmada para autorizar el descuento. \n' \
            'Informamos que la entrega del equipo debe ser autorizada previamente por el departamento de Remuneraciones. \n' \
            'Si tiene alguna duda, por favor contáctenos. \n'
            'Saludos cordiales, \n \n \n'
            'Equipo de Soporte Técnico.',
            from_email='soporte.ti@galilea.cl',
            to=[usuario.correo],
            cc=[
                'luis.caro@galilea.cl',
                'jeremy.valencia@galilea.cl',
                'carlos.munoz@galilea.cl',
                'felipe.carreno@galilea.cl',
                # soporte.ti@galilea.cl también puedes agregar aquí si quieres
            ]
        )
        email.attach('autorizacion_descuento.pdf', pdf_file.getvalue(), 'application/pdf')

        try:
            email.send(fail_silently=False)
        except Exception as e:
            print(f"Error al enviar correo: {e}")
            raise  # permite que el view capture y muestre mensaje de error

from django.db import models
from django.utils import timezone
from .modelo_equipo import Modelo_equipo
from .procesador import Procesador
from .estado_equipo import Estado_equipo
from .sistema_operativo import Sistema_operativo
from ventas.models.venta import Venta
from usuarios.models import Usuario  # Asegúrate que esta línea esté al inicio del archivo
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
from django.db import models
from django.utils.timezone import now 

# Clase Equipo.

class Equipo(models.Model):
    etiqueta = models.CharField(max_length=100, unique=True)
    memoria_ram = models.IntegerField(null=True)
    almacenamiento = models.IntegerField(null=True)
    numero_serie = models.CharField(max_length=100, null=True)
    fecha_de_compra = models.DateField(null=True, blank=True, default=now) #se puede asociar con el registro de la factura o sea se puede obtener este dato de ahí
    imei = models.CharField(max_length=100, null=True) #solo para dispositivos moviles
    mac = models.CharField(max_length=100, null=True) #solo para equipos
    en_bodega = models.BooleanField(default=True) #si el equipo se encuentra en bodega o no
    modelo = models.ForeignKey(Modelo_equipo, on_delete=models.SET_NULL, null=True )
    sistema_operativo = models.ForeignKey(Sistema_operativo, on_delete=models.SET_NULL, null=True )
    procesador = models.ForeignKey(Procesador, on_delete=models.SET_NULL, null=True )
    estado = models.ForeignKey(Estado_equipo, on_delete=models.SET_NULL, null=True )
    usuario_asignado = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)
    ubicacion = models.ForeignKey('Ubicacion', on_delete=models.SET_NULL, null=True, blank=True)  # NUEVO
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)  # NUEVO



    def __str__(self):
        return self.etiqueta

    def cambiar_estado(self, nuevo_estado):
        from .equipo_historial import Equipo_historial

        if self.pk:
            estado_actual = Equipo.objects.get(pk=self.pk).estado
        else:
            estado_actual = None

        if estado_actual != nuevo_estado:
            Equipo_historial.objects.create(
                equipo=self,
                fecha=timezone.now(),
                estado_anterior=estado_actual,
                nuevo_estado=nuevo_estado
            )
        self.estado = nuevo_estado

    def modificar_equipo(self, form, modificado_por=None):
        from .equipo_historial import Equipo_historial
        from django.utils import timezone

        cambios = []
        estado_anterior = self.estado

        for campo, nuevo_valor in form.cleaned_data.items():
            valor_actual = getattr(self, campo)

            # Comparación robusta para ForeignKey y otros tipos
            if str(valor_actual) != str(nuevo_valor):
                cambios.append(f"{campo}: {valor_actual} → {nuevo_valor}")
                setattr(self, campo, nuevo_valor)

        self.save()

        if cambios:
            nombre_modificador = (
                modificado_por.nombre_completo
                if modificado_por and hasattr(modificado_por, 'nombre_completo')
                else str(modificado_por or "desconocido")
            )

            observaciones = f"Modificado por {nombre_modificador}\n" + "\n".join(cambios)

            Equipo_historial.objects.create(
                equipo=self,
                fecha=timezone.now(),
                estado_anterior=estado_anterior,
                nuevo_estado=self.estado,
                observaciones=observaciones
            )





    def eliminar_equipo(self):
        self.delete()


    def aprobar_por_rrhh(self):
        from inventario.models.estado_equipo import Estado_equipo
        from ventas.models.venta import Venta

        self.estado_id = 8  # ID de "Pendiente de entrega"
        self.save()

        venta = Venta.objects.filter(id_equipo=self).first()
        if venta:
            venta.flag_aprobado_remuneraciones = True
            venta.save()


    def rechazar_por_rrhh(self):
        from inventario.models.estado_equipo import Estado_equipo

        self.estado_id = 6  # ID de "Activo" o "Por vender"
        self.en_bodega = True
        self.save()
        venta = Venta.objects.filter(id_equipo=self).first()
        if venta:
            venta.flag_aprobado_remuneraciones = False
            venta.save()

    def generar_qr(self):
        # URL que debe abrir el QR, ajusta si cambia tu ruta
        qr_data = f"http://127.0.0.1:8000/asociacion/?equipo={self.etiqueta}"

        qr = qrcode.make(qr_data)
        buffer = BytesIO()
        qr.save(buffer, format='PNG')
        filename = f'{self.etiqueta}_qr.png'
        self.qr_code.save(filename, ContentFile(buffer.getvalue()), save=False)

    def save(self, *args, **kwargs):
        # Asignar ubicación "En Bodega" si el equipo está en bodega y no tiene ubicación aún
        if self.en_bodega and not self.ubicacion:
            from .ubicacion import Ubicacion  # Import tardío para evitar import circular
            try:
                self.ubicacion = Ubicacion.objects.get(nombre__iexact="En Bodega")
            except Ubicacion.DoesNotExist:
                pass  # Si no existe, no hace nada (o puedes crearla si quieres)

        super().save(*args, **kwargs)  # Guarda primero

        # Generar QR si aún no existe
        if not self.qr_code:
            self.generar_qr()
            super().save(update_fields=["qr_code"])

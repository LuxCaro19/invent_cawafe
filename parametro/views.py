from django.shortcuts import render, redirect, get_object_or_404
from .models import SalaVenta, Obra

def parametro_home(request):
    return render(request, 'parametro/home.html')

def salas_listar(request):
    salas = SalaVenta.objects.all()
    return render(request, 'parametro/salas_listar.html', {'salas': salas})

def sala_crear(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        SalaVenta.objects.create(nombre=nombre)
        return redirect('salas_listar')
    return render(request, 'parametro/salas_form.html', {'titulo': 'Agregar Sala', 'sala': {}})

def sala_editar(request, sala_id):
    sala = get_object_or_404(SalaVenta, id=sala_id)
    if request.method == 'POST':
        sala.nombre = request.POST.get('nombre')
        sala.save()
        return redirect('salas_listar')
    return render(request, 'parametro/salas_form.html', {'titulo': 'Editar Sala', 'sala': sala})

def sala_eliminar(request, sala_id):
    sala = get_object_or_404(SalaVenta, id=sala_id)
    sala.delete()
    return redirect('salas_listar')

def obras_listar(request):
    obras = Obra.objects.all()
    return render(request, 'parametro/obras_listar.html', {'obras': obras})

def obra_crear(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        Obra.objects.create(nombre=nombre)
        return redirect('obras_listar')
    return render(request, 'parametro/obras_form.html', {'titulo': 'Agregar Obra', 'obra': {}})

def obra_editar(request, obra_id):
    obra = get_object_or_404(Obra, id=obra_id)
    if request.method == 'POST':
        obra.nombre = request.POST.get('nombre')
        obra.save()
        return redirect('obras_listar')
    return render(request, 'parametro/obras_form.html', {'titulo': 'Editar Obra', 'obra': obra})

def obra_eliminar(request, obra_id):
    obra = get_object_or_404(Obra, id=obra_id)
    obra.delete()
    return redirect('obras_listar')
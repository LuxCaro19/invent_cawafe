# Generated by Django 5.1.7 on 2025-03-19 23:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EstadoEquipo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField()),
            ],
        ),
        migrations.CreateModel(
            name='ModeloEquipo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField()),
                ('precio', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Procesador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField()),
                ('compania', models.CharField()),
            ],
        ),
        migrations.CreateModel(
            name='SistemaOperativo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField()),
                ('compania', models.CharField()),
            ],
        ),
        migrations.CreateModel(
            name='Equipos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('etiqueta', models.CharField()),
                ('memoria_ram', models.IntegerField(null=True)),
                ('almacenamiento', models.IntegerField(null=True)),
                ('estado', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventario.estadoequipo')),
                ('modelo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventario.modeloequipo')),
                ('procesador', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventario.procesador')),
                ('sistema_operativo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventario.sistemaoperativo')),
            ],
        ),
    ]

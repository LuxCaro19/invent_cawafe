# Generated by Django 5.1.7 on 2025-03-22 20:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0004_modelo_modelo_tipo_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Modelo_modelo_marca',
            new_name='Modelo_marca',
        ),
        migrations.RenameModel(
            old_name='Modelo_modelo_tipo',
            new_name='Modelo_tipo',
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-12 08:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20161212_0723'),
    ]

    operations = [
        migrations.CreateModel(
            name='AlertaAlumno',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contenido', models.CharField(max_length=500)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Alumno')),
            ],
            options={
                'verbose_name_plural': 'Alertas',
            },
        ),
    ]
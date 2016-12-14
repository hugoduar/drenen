from __future__ import unicode_literals
from django.contrib.auth.models import User


from django.db import models


class Lugar(models.Model):
    nombre = models.CharField(max_length=500)
    class Meta:
        verbose_name_plural = "Lugares"
    def __unicode__(self):
        return "%s" % (self.nombre)

class Alumno(models.Model):
    user = models.OneToOneField(User)
    email = models.CharField(max_length=500)
    escuela = models.CharField(max_length=500)
    carrera = models.CharField(max_length=500)
    grupo = models.CharField(max_length=500)
    boleta = models.CharField(max_length=500)
    nombre = models.CharField(max_length=500)
    apellido_paterno = models.CharField(max_length=500)
    apellido_materno = models.CharField(max_length=500)
    telefono = models.CharField(max_length=500)
    inicio = models.DateField(default=None,blank=True, null=True)
    termino = models.DateField(default=None,blank=True, null=True)
    lugar = models.ForeignKey(Lugar, blank=True, null=True,default=None)
    class Meta:
        verbose_name_plural = "Alumnos"
    def __unicode__(self):
        return "%s %s %s" % (self.nombre, self.apellido_paterno, self.apellido_materno) 


class Coordinador(models.Model):
    user = models.OneToOneField(User)
    nombre = models.CharField(max_length=500)
    identificador = models.CharField(max_length=500)
    class Meta:
        verbose_name_plural = "Coordinadores"
    def __unicode__(self):
        return "%s" % (self.nombre)


class Administrador(models.Model):
    user = models.OneToOneField(User)
    nombre = models.CharField(max_length=500)
    identificador = models.CharField(max_length=500)
    class Meta:
        verbose_name_plural = "Administradores"
    def __unicode__(self):
        return "%s" % (self.nombre)

class Reporte(models.Model):
    alumno = models.ForeignKey(Alumno)
    fecha = models.DateField(auto_now_add=True)
    titulo = models.CharField(max_length=1000)
    descripcion = models.CharField(max_length=3000)
    status = models.BooleanField(default=False)
    imagen = models.ImageField(null=True, blank=True)
    class Meta:
        verbose_name_plural = "Reportes"
    def __unicode__(self):
        return "%s %s" % (self.alumno, self.titulo)

class Entrada(models.Model):
    titulo = models.CharField(max_length=500)
    contenido = models.TextField()
    imagen = models.ImageField(null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True, null=True)
    class Meta:
        verbose_name_plural = "Entradas"
    def __unicode__(self):
        return "%s" % (self.titulo)


class AlertaAlumno(models.Model):
    contenido = models.CharField(max_length=500)
    user = models.ForeignKey(User)
    class Meta:
        verbose_name_plural = "Alertas"
    def __unicode__(self):
        return "%s" % (self.contenido)   

class Configuracion(models.Model):
    logo = models.ImageField(null=True, blank=True)
    color_fondo = models.CharField(max_length=6)
    class Meta:
        verbose_name_plural = "Configuraciones"
    def __unicode__(self):
        return "Configuracion"



        
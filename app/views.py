from django.shortcuts import render
from django.template import RequestContext


from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from app.forms import *
from app.models import *



from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def home(request):
	context = RequestContext(request)
	entradas = Entrada.objects.all()[:3]
	return render(request, 'SLanding/index.html', context={"entradas":entradas})

def faq(request):
	context = RequestContext(request)
	return render(request, 'SLanding/FAQ.html', context={})

def contacto(request):
	context = RequestContext(request)
	return render(request, 'SLanding/contacto.html', context={})


def home_alumno(request):
	context = RequestContext(request)
	if request.user.is_active:
		alumno = Alumno.objects.get(user=request.user)
		num_reportes = Reporte.objects.filter(alumno=alumno).count()

	return render(request, 'SAlumno/index.html', context={"alumno":alumno, "num_reportes":num_reportes})

def reporte(request):
	context = RequestContext(request)
	reporte_form = ReporteForm(data=request.POST)
	reporte = reporte_form.save(commit=False)
	reporte.alumno = Alumno.objects.get(user=request.user)
	reporte.save()
	
	return HttpResponseRedirect('/alumno')




def home_coordinador(request):
	context = RequestContext(request)
	alumnos = []
	alumnos_atrasados = []
	alumnos_from_db = Alumno.objects.all()
	for alumno in alumnos_from_db:
		num_reportes = Reporte.objects.filter(alumno=alumno).count()
		num_reportes_atrasados = Reporte.objects.filter(alumno=alumno, status=False).count()
		alumno.num_reportes = num_reportes 

	 	alumnos.append(alumno)

	 	if num_reportes_atrasados>0:
	 		alumno.num_reportes_atrasados = num_reportes_atrasados 
	 		alumnos_atrasados.append(alumno)

	return render(request, 'SCoordinador/index.html', context={"alumnos":alumnos, "alumnos_atrasados":alumnos_atrasados})

def home_administrador(request):
	context = RequestContext(request)
	return render(request, 'SAdministrador/index.html', context={})

def register(request):
    context = RequestContext(request)
    username = request.POST['username']
    password = request.POST['password1']
    if request.method == 'POST':
    	form = UserForm(data=request.POST)
        alumno_form = AlumnoForm()
        if form.is_valid():
            user = form.save()
            #user.set_password(user.password)
            user.save()

            alumno = alumno_form.save(commit=False)
            alumno.email = request.POST['email']
            alumno.escuela = request.POST['escuela']
            alumno.carrera = request.POST['carrera']
            alumno.grupo = request.POST['grupo']
            alumno.boleta = request.POST['boleta']
            alumno.nombre = request.POST['nombre']
            alumno.apellido_paterno = request.POST['apellido_paterno']
            alumno.apellido_materno = request.POST['apellido_materno']
            alumno.telefono = request.POST['telefono']

            alumno.user = user

            alumno.save()
            user2 = authenticate(username=username, password=password)        
            if user2 is not None:
                if user.is_active:
                    auth_login(request, user2)
                    return HttpResponseRedirect('/')
                else:
                    pass
            else:
                return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/')
    else:
        form = UserForm()
        return HttpResponseRedirect('/')

def login(request):
    context = RequestContext(request)
    user = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return HttpResponseRedirect('/alumno')
            else:
                pass
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return render_to_response("SLanding/index.html", {"error": True, "username": username}, context)
    elif request.method == 'GET' and user is None: 
		return render_to_response("SLanding/index.html", {"error": False}, context)
    else:
    	return render_to_response("SLanding/index.html", {"error": True}, context)



def logout(request):
    context = RequestContext(request)
    auth_logout(request)
    return HttpResponseRedirect('/')







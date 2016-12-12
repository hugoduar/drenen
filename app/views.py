from django.shortcuts import render
from django.template import RequestContext


from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404

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
	entradas = Entrada.objects.all().order_by('-fecha')[:3]
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
		alertas = AlertaAlumno.objects.filter(user=request.user)

	return render(request, 'SAlumno/index.html', context={"alumno":alumno, "num_reportes":num_reportes, "alertas":alertas})

def reporte(request):
	context = RequestContext(request)
	reporte_form = ReporteForm(request.POST, request.FILES)
	reporte = reporte_form.save(commit=False)
	reporte.alumno = Alumno.objects.get(user=request.user)
	reporte.save()
	
	return HttpResponseRedirect('/alumno')

def aprobar_reporte(request):
	context = RequestContext(request)
	reporte = Reporte.objects.get(id=request.POST['id_reporte'])
	reporte.status = True
	reporte.save()
	AlertaAlumno.objects.filter(user=reporte.alumno.user).delete()
	return HttpResponseRedirect('/coordinador')



def home_coordinador(request):
	context = RequestContext(request)
	alumnos = []
	alumnos_atrasados = []
	alumnos_from_db = Alumno.objects.all()
	ent = True
	entradas = Entrada.objects.all()
	reportes = Reporte.objects.filter(status=False)
	for alumno in alumnos_from_db:
		num_reportes = Reporte.objects.filter(alumno=alumno).count()
		num_reportes_atrasados = Reporte.objects.filter(alumno=alumno, status=False).count()
		alumno.num_reportes = num_reportes 

	 	alumnos.append(alumno)

	 	if num_reportes_atrasados>0:
	 		alumno.num_reportes_atrasados = num_reportes_atrasados 
	 		alumnos_atrasados.append(alumno)
    
	return render(request, 'SCoordinador/index.html', context={"alumnos":alumnos, "alumnos_atrasados":alumnos_atrasados, "entradas":entradas, "ent":ent, "reportes":reportes})

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

def noticia(request, num):
	context = RequestContext(request)
	entrada = Entrada.objects.get(pk=num)
	return render_to_response("SLanding/noticia_detail.html", {"entrada": entrada}, context)

def entrada(request):
    context = RequestContext(request)
    entrada_form = EntradaForm(request.POST, request.FILES)
    entrada = entrada_form.save(commit=False)
    entrada.save()
    return HttpResponseRedirect('/coordinador')
def modificar_entrada(request):
    obj = get_object_or_404(Entrada, pk=request.POST['id_entrada'])
    form = EntradaForm(request.POST or None,
                        request.FILES or None, instance=obj)
    if request.method == 'POST':
        if form.is_valid():
           form.save()
           return redirect('/coordinador')
    return HttpResponseRedirect('/coordinador')

def eliminar_entrada(request):
    context = RequestContext(request)
    entrada = Entrada.objects.get(id=request.POST['id_entrada'])
    entrada.delete()
    return HttpResponseRedirect('/coordinador#menu2')

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
                if Alumno.objects.filter(user=user).exists():
                	request.session['user_type'] = 'alumno'
                	return HttpResponseRedirect('/alumno')
                elif Coordinador.objects.filter(user=user).exists():
                	request.session['user_type'] = 'coordinador'
                	return HttpResponseRedirect('/coordinador')

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


def enviar_alerta(request):
	context = RequestContext(request)
	user  = User.objects.get(id=request.POST['id_user'])
	alerta = AlertaAlumno()
	alerta.contenido = 'REPORTE ATRASADO!'
	alerta.user = user
	alerta.save()
	return HttpResponseRedirect('/coordinador')





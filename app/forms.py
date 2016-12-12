from django import forms
from django.contrib.auth.models import User

from app.models import *

from django.utils.translation import ugettext, ugettext_lazy as _

class UserForm(forms.ModelForm):
   	error_messages = {
        'duplicate_username': _("El nombre de usuario ya existe."),
        'password_mismatch': _("Las dos password no coincidieron."),
    }
   	username = forms.RegexField(label=_("Username"), max_length=30,
        regex=r'^[\w.@+-]+$',
        help_text=_("Menos de 30 caracteres"),
        error_messages={
            'invalid': _("Solo letras, numeros y "
                         "@/./+/-/_ caracteres.")})
   	password1 = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput)
   	password2 = forms.CharField(label=_("Repetir password"),
        widget=forms.PasswordInput,
        help_text=_("Introduce la misma password."))

   	class Meta:
   		model = User
   		fields = ("username", )

   	def clean_username(self):
     
		# Since User.username is unique, this check is redundant,
     
		# but it sets a nicer error message than the ORM. See #13147.
		username = self.cleaned_data["username"]
     
		try:
			User._default_manager.get(username=username)
     
		except User.DoesNotExist:
			return username
     
		raise forms.ValidationError(
            self.error_messages['duplicate_username'],
            code='duplicate_username',
        )
	def clean_password2(self):
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError(self.error_messages['password_mismatch'],code='password_mismatch',)
		return password2

	def save(self, commit=True):
		user = super(UserForm, self).save(commit=False)
		user.set_password(self.cleaned_data["password1"])
		if commit:
			user.save()
		return user

class AlumnoForm(forms.ModelForm):
  class Meta:
    model = Alumno
    fields = "__all__" 


class ReporteForm(forms.ModelForm):
  class Meta:
    model = Reporte
    fields = ['titulo', 'descripcion', 'imagen']


class EntradaForm(forms.ModelForm):
  class Meta:
    model = Entrada
    fields =['titulo', 'contenido', 'imagen']

class AlertaAlumnoForm(forms.ModelForm):
  class Meta:
    model = AlertaAlumno
    fields = "__all__" 














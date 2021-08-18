from django import forms
from django.forms import Form, ModelForm
from sispro.models import Protagonista


# Formulario de autenticación
class LoginForm(Form):
	nombreusuario = forms.CharField(max_length=25,label='Nombre de Usuario')
	contrasena = forms.CharField(max_length=25,widget=forms.PasswordInput,label='Contraseña') 



# Formulario de edición de Protagonistas
class ProtagonistaForm(ModelForm):

	class Meta:
		model = Protagonista
		fields = ['cedula','nombres','apellidos','fecha_nacimiento','sexo','etnia','comunidad','telefono','promotor','jvc']
		widgets = {
			'cedula':forms.TextInput(attrs={'readonly':True})
		}


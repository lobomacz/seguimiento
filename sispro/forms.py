from django import forms


# Formulario de autenticación
class LoginForm(forms.Form):
	nombreusuario = forms.CharField(max_length=25,label='Nombre de Usuario')
	contrasena = forms.CharField(max_length=25,widget=forms.PasswordInput,label='Contraseña') 
from django.contrib.admin import AdminSite, ModelAdmin, TabularInline, StackedInline
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group, Permission
from sispro.models import Tabla, DetalleTabla, Municipio, Comunidad, Institucion, Contacto, Programa, Proyecto, Bono, Protagonista

# Registro de modelos administrados


#	  _________.___   ___________________ __________ ________   
#	 /   _____/|   | /   _____/\______   \\______   \\_____  \  																																																																																				
#	 \_____  \ |   | \_____  \  |     ___/ |       _/ /   |   \ 
#	 /        \|   | /        \ |    |     |    |   \/    |    \
#	/_______  /|___|/_______  / |____|     |____|_  /\_______  /
#	        \/              \/                    \/         \/ 

# AdminSite de la aplicación sispro

class SisproAdmin(AdminSite):

	site_header = 'Administración del sistema SISPRO'
	site_title = 'Admin SISPRO'
	index_title = site_title
	site_url = None


class DetalleTablaInline(TabularInline):
	model = DetalleTabla
	ordering = ['elemento']


class TablaAdmin(ModelAdmin):
	model = Tabla
	inlines = [
		DetalleTablaInline,
	]
	ordering = ['tabla']


class ComunidadInline(TabularInline):
	model = Comunidad
	ordering = ['nombre']


class MunicipioAdmin(ModelAdmin):
	model = Municipio
	inlines = [
		ComunidadInline,
	]
	ordering = ['nombre']


class ProyectoInline(TabularInline):
	model = Proyecto 
	ordering = ['nombre']


class ProgramaAdmin(ModelAdmin):
	model = Programa
	inlines = [
		ProyectoInline,
	]
	ordering = ['sector','institucion','nombre']


class SisproUserAdmin(UserAdmin):
	model = User

	


sispro_admin = SisproAdmin(name='sisproadmin')

sispro_admin.register(Tabla, TablaAdmin)
sispro_admin.register(Municipio, MunicipioAdmin)
sispro_admin.register(Programa, ProgramaAdmin)
sispro_admin.register(Institucion)
sispro_admin.register(Contacto) 
sispro_admin.register(Proyecto)
sispro_admin.register(Bono)
sispro_admin.register(Protagonista)
sispro_admin.register(User, SisproUserAdmin)
sispro_admin.register(Group)
sispro_admin.register(Permission)



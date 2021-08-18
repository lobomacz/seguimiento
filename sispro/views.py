from django.shortcuts import get_object_or_404, get_list_or_404, render, redirect
from django.urls import reverse_lazy
from django.conf import settings
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View 
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, FormView
from sispro.models import *
from sispro.forms import LoginForm, ProtagonistaForm
import datetime


# Create your views here.


PAGINAS = settings.SISPRO_CONF['paginas']


# Vistas genéricas


# Clase genérica para crear/editar registros
class SisproCreateEditView(LoginRequiredMixin):

	def get_context_data(self, **kwargs):

		context = super().get_context_data(**kwargs)
		context['usuario'] = self.request.user
		context['fecha'] = datetime.date.today()

		return context



# Vista genérica para listas
class SisproListView(SisproCreateEditView, ListView):

	paginate_by = PAGINAS

	def get_context_data(self, **kwargs):

		context = super().get_context_data(**kwargs)

		paginator = context['paginator'] # self.get_paginator(self.queryset,self.paginate_by)
		context['rango_paginas'] = paginator.get_elided_page_range(self.request.GET.get('page', 1),on_each_side=2)

		return context



# Vista genérica para detalle de objetos
class SisproDetailView(SisproCreateEditView, DetailView):

	def get_context_data(self, **kwargs):

		context = super().get_context_data(**kwargs)

		return context




# Vistas principales

# Vista de ingreso de usuarios(login)
class LoginView(FormView):

	template_name = 'sispro/login.html'
	form_class = LoginForm
	success_url = reverse_lazy('inicio_sispro')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['fecha'] = datetime.date.today()

		return context


	def form_valid(self, form):

		data = form.cleaned_data
		username = data['nombreusuario']
		password = data['contrasena']
		usuario = authenticate(self.request, username=username, password=password)

		if usuario is not None:
			login(self.request, usuario)
			return super().form_valid(form)
		else:
			return super().form_invalid(form)


# Vista de salida de usuarios(logout)
class LogoutView(View):

	def get(self, request, *args, **kwargs):
		logout(request)
		return redirect('inicio_sispro')



# Vista de la página de inicio
class InicioView(TemplateView):

	template_name = 'sispro/inicio.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['usuario'] = self.request.user
		context['fecha'] = datetime.date.today()

		return context


# Vista de mensaje de error
class ErrorView(InicioView):

	template_name = 'sispro/error.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		tipo_error = settings.SISPRO_CONF['tipos-error'][int(self.request.GET.get('t'))]
		mensaje = settings.SISPRO_CONF['mensajes-error'][self.request.GET.get('m')]
		context['tipo_error'] = tipo_error.upper()
		context['mensaje'] = mensaje.upper()

		return context


# Lista de Programas
class ListaProgramasView(SisproListView):

	template_name = 'sispro/lista_programas.html'
	model = Programa 
	context_object_name = 'lista_programas'


# Detalle de Programa
class DetalleProgramaView(SisproDetailView):

	template_name = 'sispro/detalle_programa.html'
	model = Programa
	context_object_name = 'programa'


# Lista de Proyectos
class ListaProyectosView(SisproListView):

	template_name = 'sispro/lista_proyectos.html'
	model = Proyecto
	context_object_name = 'lista_proyectos'


# Detalle de Proyecto
class DetalleProyectoView(SisproDetailView):

	template_name = 'sispro/detalle_proyecto.html'
	model = Proyecto
	context_object_name = 'proyecto'


# Pagina Menu Protagonistas
class MenuProtagonistasView(InicioView):

	template_name = 'sispro/menu_protagonistas.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['url_protagonistas'] = reverse_lazy('lista_protagonistas')
		context['url_planes_inversion'] = reverse_lazy('lista_planes_inversion')
		context['url_bonos'] = reverse_lazy('lista_bonos')

		return context



# Lista de Protagonistas
class ListaProtagonistasView(SisproListView):

	template_name = 'sispro/lista_protagonistas.html'
	queryset = Protagonista.objects.all()
	context_object_name = 'lista_protagonistas'

	def get_context_data(self, **kwargs):

		context = super().get_context_data(**kwargs)
		context['buscar'] = True
		context['ruta'] = reverse_lazy('lista_filtro_protagonistas')

		return context


# Lista de Búsqueda de Protagonistas
class ListaFiltroProtagonistasView(ListaProtagonistasView):

	def get_queryset(self):

		clave = self.request.GET.get('q').replace('-','')

		return Protagonista.objects.filter(pk=clave)



# Detalle de Protagonista
class DetalleProtagonistaView(SisproDetailView):

	template_name = 'sispro/detalle_protagonista.html'
	model = Protagonista
	context_object_name = 'protagonista'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		protagonista = self.get_object()
		context['planes'] = protagonista.protagonistabono_set.filter(bono__tipo__elemento='plan de inversion')
		context['bonos'] = protagonista.protagonistabono_set.filter(bono__tipo__elemento='bono')

		return context


# Ingreso de Protagonista
class CreateProtagonistaView(SisproCreateEditView, CreateView):

	#template_name = 'sispro/create_protagonista_form.html'
	model = Protagonista
	fields = [
		'cedula',
		'nombres',
		'apellidos',
		'fecha_nacimiento',
		'sexo',
		'etnia',
		'comunidad',
		'telefono',
		'promotor',
		'jvc'
		]
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['url'] = reverse_lazy('nuevo_protagonista')

		return context

	def form_valid(self, form):
		form.instance.digitador = self.request.user
		return super().form_valid(form)




# Modificación de Protagonista
class UpdateProtagonistaView(SisproCreateEditView, UpdateView):

	#template_name = 'sispro/update_protagonista_form.html'
	model = Protagonista
	#fields = ['nombres','apellidos','fecha_nacimiento','sexo','etnia','comunidad','telefono','promotor','jvc']
	form_class = ProtagonistaForm


	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['url'] = reverse_lazy('update_protagonista', kwargs={'pk':self.kwargs['pk']})

		return context




# Lista de Bonos entregados
class ListaBonosView(SisproListView):

	template_name = 'sispro/lista_bonos.html'
	queryset = ProtagonistaBono.objects.filter(bono__tipo__elemento='bono')
	context_object_name = 'lista_bonos'

	def get_context_data(self, **kwargs):

		context = super().get_context_data(**kwargs)
		context['buscar'] = True
		context['ruta'] = reverse_lazy('lista_filtro_bonos')
		context['tipo'] = 'bono'

		return context


# Lista de Búsqueda de Bonos entregados
class ListaFiltroBonosView(ListaBonosView):

	def get_queryset(self):

		clave = self.request.GET.get('q').replace('-','')

		return ProtagonistaBono.objects.filter(cedula=clave, bono__tipo__elemento='bono')



# Detalle de Bono entregado
class DetalleBonoView(SisproDetailView):

	template_name = 'sispro/detalle_bono.html'
	model = ProtagonistaBono
	#context_object_name = 'bono'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['tipo'] = 'bono'

		return context


# Ingresa entrega de Bono a Protagonista
class CreateBonoView(SisproCreateEditView, CreateView):

	#template_name = 'sispro/entrega_bono_form.html'
	model = ProtagonistaBono
	#exclude = ['digitador']
	fields = [
		'protagonista',
		'bono','proyecto',
		'fecha_recibido',
		'tecnico',
		'comunidad',
		'coord_x',
		'coord_y',
		'altura',
		'observaciones'
		]


	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['url'] = reverse_lazy('nuevo_bono')
		context['tipo'] = 'bono'

		return context

	def form_valid(self, form):
		form.instance.digitador = self.request.user
		return super().form_valid(form)


# Edita entrega de Bono a Protagonista
class UpdateBonoView(SisproCreateEditView, UpdateView):

	#template_name = 'sispro/update_bono_form.html'
	model = ProtagonistaBono
	#exclude = ['digitador']
	fields = [
		'protagonista',
		'bono','proyecto',
		'fecha_recibido',
		'tecnico',
		'comunidad',
		'coord_x',
		'coord_y',
		'altura',
		'observaciones',
		'activo'
		]

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['url'] = reverse_lazy('update_bono', kwargs={'pk':self.kwargs['pk']})
		context['tipo'] = 'bono'

		return context


	def form_valid(self, form):
		if form.instance.digitador == self.request.user:
			return super().form_valid(form)
		else:
			raise PermissionDenied('El usuario no es el propietario.')


# Lista de Planes de Inversión entregados
class ListaPlanesInversionView(SisproListView):

	template_name = 'sispro/lista_bonos.html'
	queryset = ProtagonistaBono.objects.filter(bono__tipo__elemento='plan de inversion')
	context_object_name = 'lista_bonos'

	def get_context_data(self, **kwargs):

		context = super().get_context_data(**kwargs)
		context['buscar'] = True
		context['ruta'] = reverse_lazy('lista_filtro_planes_inversion')
		context['tipo'] = 'plan'

		return context


# Lista de Búsqueda de Planes de Inversión entregados
class ListaFiltroPlanesInversionView(ListaPlanesInversionView):

	def get_queryset(self):

		clave = self.request.GET.get('q').replace('-','')

		return ProtagonistaBono.objects.filter(cedula=clave, bono__tipo__elemento='plan de inversion')


# Detalle de Plan de Inversión entregado
class DetallePlanInversionView(SisproDetailView):

	template_name = 'sispro/detalle_bono.html'
	model = ProtagonistaBono
	#context_object_name = 'plan_inversion'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['tipo'] = 'plan'

		return context


# Ingresar entrega de Plan de Inversión a Protagonista
class CreatePlanInversionView(SisproCreateEditView, CreateView):

	#template_name = 'sispro/entrega_plan_inversion_form.html'
	model = ProtagonistaBono
	fields = [
		'protagonista',
		'bono','proyecto',
		'fecha_recibido',
		'tecnico',
		'comunidad',
		'coord_x',
		'coord_y',
		'altura',
		'observaciones'
		]
	#exclude = ['digitador']

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['url'] = reverse_lazy('nuevo_plan_inversion')
		context['tipo'] = 'plan'

		return context


	def form_valid(self, form):
		form.instance.digitador = self.request.user
		return super().form_valid(form)


# Editar entrega de Plan de Inversión a Protagonista
class UpdatePlanInversionView(SisproCreateEditView, UpdateView):

	#template_name = 'sispro/update_plan_inversion_form.html'
	model = ProtagonistaBono
	#exclude = ['digitador']
	fields = [
		'protagonista',
		'bono','proyecto',
		'fecha_recibido',
		'tecnico',
		'comunidad',
		'coord_x',
		'coord_y',
		'altura',
		'observaciones',
		'activo'
		]


	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['url'] = reverse_lazy('update_plan_inversion', kwargs={'pk':self.kwargs['pk']})
		context['tipo'] = 'plan'

		return context


	def form_valid(self, form):
		if form.instance.digitador == self.request.user:
			return super().form_valid(form)
		else:
			raise PermissionDenied('El usuario no es el propietario.')







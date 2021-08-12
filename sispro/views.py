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
from sispro.forms import LoginForm
import datetime


# Create your views here.


PAGINAS = settings.SISPRO_CONF['paginas']


# Vistas genéricas

# Vista genérica para listas
class SisproListView(LoginRequiredMixin, ListView):

	paginate_by = PAGINAS

	def get_context_data(self, **kwargs):

		context = super().get_context_data(**kwargs)
		context['usuario'] = self.request.user
		context['fecha'] = datetime.date.today()
		paginator = self.get_paginator(self.queryset,self.paginate_by)
		context['rango_paginas'] = paginator.get_elided_page_range(self.request.GET.get('page', 1),on_each_side=2)

		return context



# Vista genérica para detalle de objetos
class SisproDetailView(LoginRequiredMixin, DetailView):

	def get_context_data(self, **kwargs):

		context = super().get_context_data(**kwargs)
		context['usuario'] = self.request.user
		context['fecha'] = datetime.date.today()

		return context


# Vista genérica para crear registros
class SisproCreateView(LoginRequiredMixin, CreateView):

	def get_context_data(self, **kwargs):

		context = super().get_context_data(**kwargs)
		context['usuario'] = self.request.user
		context['fecha'] = datetime.date.today()

		return context


# Vista genérica para editar registros
class SisproUpdateView(LoginRequiredMixin, UpdateView):

	def get_context_data(self, **kwargs):

		context = super().get_context_data(**kwargs)
		context['usuario'] = self.request.user
		context['fecha'] = datetime.date.today()

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


	def form_valid(self,form):
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
class CreateProtagonistaView(SisproCreateView):

	template_name = 'sispro/create_protagonista_form.html'
	model = Protagonista
	fields = '__all__'


# Modificación de Protagonista
class UpdateProtagonistaView(SisproUpdateView):

	template_name = 'sispro/update_protagonista_form.html'
	model = Protagonista
	exclude = ['cedula']


# Lista de Bonos entregados
class ListaBonosView(SisproListView):

	template_name = 'sispro/lista_bonos.html'
	queryset = ProtagonistaBono.objects.filter(bono__tipo__elemento='bono')
	context_object_name = 'lista_bonos'

	def get_context_data(self, **kwargs):

		context = super().get_context_data(**kwargs)
		context['buscar'] = True
		context['ruta'] = reverse_lazy('lista_filtro_bonos')
		context['clave_buscar'] = 'cedula'

		return context


# Lista de Búsqueda de Bonos entregados
class ListaFiltroBonosView(ListaBonosView):

	def get_queryset(self):

		clave = self.kwargs['cedula'].replace('-','')

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
class CreateBonoView(SisproCreateView):

	template_name = 'sispro/entrega_bono_form.html'
	model = ProtagonistaBono
	exclude = ['digitador']

	def form_valid(self, form):
		form.instance.digitador = self.request.user
		return super().form_valid(form)


# Edita entrega de Bono a Protagonista
class UpdateBonoView(SisproUpdateView):

	template_name = 'sispro/update_bono_form.html'
	model = ProtagonistaBono
	exclude = ['digitador']

	def form_valid(self, form):
		if form.instance.digitador == self.request.user:
			return super().form_valid(form)
		else:
			raise PermissionDenied('El usuario no es el propietario.')


# Lista de Planes de Inversión entregados
class ListaPlanesInversionView(SisproListView):

	template_name = 'sispro/lista_planes_inversion.html'
	queryset = ProtagonistaBono.objects.filter(bono__tipo__elemento='plan de inversion')
	context_object_name = 'lista_planes'

	def get_context_data(self, **kwargs):

		context = super().get_context_data(**kwargs)
		context['buscar'] = True
		context['ruta'] = reverse_lazy('lista_filtro_planes_inversion')
		context['clave_buscar'] = 'cedula'

		return context


# Lista de Búsqueda de Planes de Inversión entregados
class ListaFiltroPlanesInversionView(ListaPlanesInversionView):

	def get_queryset(self):

		clave = self.kwargs['cedula'].replace('-','')

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
class CreatePlanInversionView(SisproCreateView):

	template_name = 'sispro/entrega_plan_inversion_form.html'
	model = ProtagonistaBono
	exclude = ['digitador']

	def form_valid(self, form):
		form.instance.digitador = self.request.user
		return super().form_valid(form)


# Editar entrega de Plan de Inversión a Protagonista
class UpdatePlanInversionView(SisproUpdateView):

	template_name = 'sispro/update_plan_inversion_form.html'
	model = ProtagonistaBono
	exclude = ['digitador']

	def form_valid(self, form):
		if form.instance.digitador == self.request.user:
			return super().form_valid(form)
		else:
			raise PermissionDenied('El usuario no es el propietario.')







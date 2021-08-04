from django.shortcuts import get_object_or_404, get_list_or_404, render
from django.urls import reverse_lazy
from django.conf import settings
from django.congrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from sispro.models import *
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



# Vista genérica para detalle de objetos
class SisproDetailView(LoginRequiredMixin, DetailView):

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['usuario'] = self.request.user


# Vista genérica para crear registros
class SisproCreateView(LoginRequiredMixin, CreateView):

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['usuario'] = self.request.user


# Vista genérica para editar registros
class SisproUpdateView(LoginRequiredMixin, UpdateView):

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['usuario'] = self.request.user



# Vistas principales

# Vista de la página de inicio
class IncioView(TemplateView):

	template_name = 'sispro/inicio.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['usuario'] = self.request.user

		return context


# Lista de Programas
class ListaProgramasView(SisproListView):

	template_name = 'sispro/lista_programas.html'
	model = Programa 


# Detalle de Programa
class DetalleProgramaView(SisproDetailView):

	template_name = 'sispro/detalle_programa.html'
	model = Programa


# Lista de Proyectos
class ListaProyectosView(SisproListView):

	template_name = 'sispro/lista_proyectos.html'
	model = Proyecto


# Detalle de Proyecto
class DetalleProyectoView(SisproDetailView):

	template_name = 'sispro/detalle_proyecto.html'
	model = Proyecto


# Lista de Protagonistas
class ListaProtagonistasView(SisproListView):

	template_name = 'sispro/lista_protagonistas.html'
	model = Protagonista


# Detalle de Protagonista
class DetalleProtagonistaView(SisproDetailView):

	template_name = 'sispro/detalle_protagonista.html'
	model = Protagonista


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


# Detalle de Bono entregado
class DetalleBonoView(SisproDetailView):

	template_name = 'sispro/detalle_bono.html'
	model = ProtagonistaBono


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
	queryset = ProtagonistaBono.objects.filter(bono__tipo__elemento='plan_inversion')


# Detalle de Plan de Inversión entregado
class DetallePlanInversionView(SisproDetailView):

	template_name = 'sispro/detalle_plan_inversion.html'
	model = ProtagonistaBono


# Ingresar entrega de Plan de Inversión a Protagonista
class CreatePlanInversionView(SisproCreateView):

	template_name = 'sispro/create_plan_inversion_form.html'
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







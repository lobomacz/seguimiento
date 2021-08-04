from django.urls import include, path
from django.conf import settings
from django.conf.static import static 
from sispro.views import *

urlpatterns = [
	path('', InicioView.as_view(), name='inicio'),
	path('programas/', ListaProgramasView.as_view(), name='lista_programas'),
	path('programas/<int:pk>/', DetalleProgramaView.as_view(), name='detalle_programa'),
	path('proyectos/', ListaProyectosView.as_view(), name='lista_proyectos'),
	path('proyectos/<int:pk>/', DetalleProyectoView.as_view(), name='detalle_proyecto'),
	path('protagonistas/', include([
		path('', ListaProtagonistasView.as_view(), name='lista_protagonistas'),
		path('crear/', CreaProtagonistaView.as_view(), name='crea_protagonista'),
		path('<str:pk>/', DetalleProtagonistaView.as_view(), name='detalle_protagonista'),
		path('<str:pk>/editar/', UpdateProtagonistaView.as_view(), name='update_protagonista'),
		])),
	path('bonos/', include([
		path('', ListaBonosView.as_view(), name='lista_bonos'),
		path('nuevo/' CreateBonoView.as_view(), name='nuevo_bono'),
		path('<int:pk>/', DetalleBonoView.as_view(), name='detalle_bono'),
		path('<int:pk>/editar/', UpdateBonoView.as_view(), name='update_bono'),
		])),
	path('planes-inversion/', include([
		path('', ListaPlanesInversionView.as_view(), name='lista_planes_inversion'),
		path('nuevo/', CreatePlanInversionView.as_view(), name='nuevo_plan_inversion'),
		path('<int:pk>/', DetallePlanInversionView.as_view(), name='detalle_plan_inversion'),
		path('<int:pk>/editar/', UpdatePlanInversionView.as_view(), name='update_plan_inversion'),
		])),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

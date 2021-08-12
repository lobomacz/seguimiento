from django.contrib.gis.db import models
from django.db.models import Q 
from django.core.validators import RegexValidator
from django.contrib.auth.models import User 
from django.urls import reverse 
from django_timestamps.softDeletion import SoftDeletionModel
from django_timestamps.timestamps import TimestampsModel


# Create your models here.


# Modelo para tablas generales

class Tabla(TimestampsModel):
	""" Clase para el modelo Tabla """
	tabla = models.CharField(max_length=25)

	def __str__(self):
		return self.tabla


# Tablas generales 

class DetalleTabla(TimestampsModel):
	""" Clase para el modelo DetalleTabla """
	elemento = models.CharField(max_length=45)
	codigo_eq = models.CharField('Código de equivalencia', max_length=15, null=True, blank=True)
	tabla = models.ForeignKey(Tabla, on_delete=models.CASCADE)

	def __str__(self):
		return self.elemento

	class Meta:
		ordering = ['tabla', 'id']
		verbose_name = 'Detalle de Tabla'
		verbose_name_plural = 'Detalles de Tabla'



# Tabla de Municipios
class Municipio(models.Model):
	"""
	Clase para el modelo Municipio.
	""" 
	nombre = models.CharField(max_length=50)
	nombre_corto = models.CharField(max_length=10)
	region = models.CharField(max_length=5, choices=[('raccs', 'Región Autónoma de la Costa Caribe Sur'),('raccn', 'Región Autónoma de la Costa Caribe Norte')], default='raccs')
	area = models.DecimalField(max_digits=8, decimal_places=2, null=True, help_text="Extensión en Km^2")
	poblacion = models.IntegerField('Población aprox.', null=True)

	def __str__(self):
		return self.nombre.upper()

	class Meta:
		ordering = ['nombre']



# Tabla de Comunidades
class Comunidad(models.Model):
	""" 
	Clase para el modelo Comunidad. Empleado como nivel por defecto de desagregación de indicadores.
	"""
	nombre = models.CharField(max_length=150)
	municipio = models.ForeignKey(Municipio, on_delete=models.RESTRICT, default=1)
	actividades_ec = models.ManyToManyField(DetalleTabla, related_name='+', help_text='Actividades económicas desarrolladas en la comunidad.', limit_choices_to=Q(tabla__tabla='actividades_ec'))
	lat = models.DecimalField('Latitud(Decimal)', max_digits=10, decimal_places=6, help_text='Latitud en notación decimal.')
	lng = models.DecimalField('Longitud(Decimal', max_digits=10, decimal_places=6, help_text='Latitud en notación decimal.')

	def __str__(self):
		return "%s-%s" % (self.municipio.nombre_corto.upper(), self.nombre.upper())

	class Meta:
		verbose_name_plural = 'Comunidades'
		ordering = ['municipio', 'nombre']



# Tabla de Instituciones
class Institucion(SoftDeletionModel, TimestampsModel):
	""" Modelo Institucion para registro de las instituciones protagonistas """

	nombre = models.CharField(max_length=150)
	siglas = models.CharField(max_length=25)
	sector = models.ForeignKey(
		DetalleTabla, 
		on_delete=models.SET_NULL, 
		null=True, 
		related_name='instituciones_sectores', 
		related_query_name='institucion_sector', 
		limit_choices_to=Q(tabla__tabla='sectores'), 
		help_text='Sector que atiende la institución.'
		)
	correo = models.EmailField(max_length=50, null=True, blank=True)
	web = models.URLField(max_length=150, null=True, blank=True)


	def __str__(self):
		return self.siglas.upper()

	class Meta:
		ordering = ['sector', 'nombre']
		verbose_name = 'Institución'
		verbose_name_plural = 'Instituciones'



# Tabla de Contactos
class Contacto(SoftDeletionModel, TimestampsModel):
	""" Modelo Contacto para el registro de contactos y técnicos de las instituciones """

	cedula = models.CharField(max_length=14, primary_key=True, help_text='Cédula de identidad sin guiones')
	nombres = models.CharField(max_length=100)
	apellidos = models.CharField(max_length=100)
	comunidad = models.ForeignKey(Comunidad, on_delete=models.RESTRICT, help_text='Comunidad de residencia')
	fecha_nacimiento = models.DateField('Fecha de nacimiento', null=True)
	sexo = models.CharField(max_length=1, choices=[('m', 'Masculino'), ('f', 'Femenino')])
	etnia = models.ForeignKey(DetalleTabla, on_delete=models.SET_NULL, null=True, limit_choices_to=Q(tabla__tabla='etnias'), related_name='contactos_etnias', related_query_name='contacto_etnia')
	telefono = models.CharField(max_length=9, help_text='8888-8888', null=True, blank=True)
	institucion = models.ForeignKey(Institucion, on_delete=models.RESTRICT)
	cargo = models.ForeignKey(DetalleTabla, on_delete=models.SET_NULL, null=True, limit_choices_to=Q(tabla__tabla='cargos'), related_name='contactos_cargos', related_query_name='contacto_cargo')
	usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, help_text='Requerido sólo si el usuario tendrá acceso a digitar o extraer datos.')
	activo = models.BooleanField(default=True)

	class Meta:
		ordering = ['institucion', 'apellidos', 'nombres']

	def __str__(self):
		return "{0} {1}".format(self.nombres.upper(), self.apellidos.upper())



# Tabla de Programas
class Programa(models.Model):
	""" Modelo Programa para el registro y agrupación de proyectos por programa. """

	codigo = models.CharField('Código', max_length=50)
	nombre = models.CharField(max_length=200)
	acronimo = models.CharField('Acrónimo', max_length=45)
	descripcion = models.TextField('Descripción', max_length=500)
	institucion = models.ForeignKey(Institucion, on_delete=models.RESTRICT)
	sector = models.ForeignKey(DetalleTabla, on_delete=models.RESTRICT, limit_choices_to=Q(tabla__tabla='sectores'))
	finalizado = models.BooleanField(default=False)

	class Meta:
		ordering = ['finalizado','sector','nombre']

	def __str__(self):
		return "{0} - {1}".format(self.codigo.upper(), self.nombre.upper())


# Tabla de Proyectos
class Proyecto(models.Model):
	""" Modelo Proyecto para el registro y agrupación de los bonos y planes de inversión. """

	codigo = models.CharField('Código', max_length=50)
	nombre = models.CharField(max_length=200)
	acronimo = models.CharField('Acrónimo', max_length=45)
	programa = models.ForeignKey(Programa, on_delete=models.SET_NULL, null=True, blank=True)
	sector = models.ForeignKey(DetalleTabla, on_delete=models.RESTRICT, limit_choices_to=Q(tabla__tabla='sectores'))
	institucion = models.ForeignKey(Institucion, on_delete=models.RESTRICT)
	contacto = models.ForeignKey(Contacto, on_delete=models.SET_NULL, null=True, blank=True)
	finalizado = models.BooleanField(default=False)

	def __str__(self):
		return "{0} - {1}".format(self.codigo.upper(), self.acronimo.upper())

	class Meta:
		ordering = ['finalizado', 'sector', 'nombre']


# Tabla de Bonos
class Bono(TimestampsModel):
	""" Modelo Bono para el registro de los diferentes bonos productivos del gobierno. """

	codigo = models.CharField('Código', max_length=50, null=True, blank=True)
	nombre = models.CharField(max_length=100)
	descripcion = models.TextField('Descripción')
	sector = models.ForeignKey(DetalleTabla, on_delete=models.RESTRICT, limit_choices_to=Q(tabla__tabla='sectores'), related_name='bonos_sectores', related_query_name='bono_sector')
	# El campo tipo clasifica si se trata de un bono o un plan de inversión 
	tipo = models.ForeignKey(DetalleTabla, on_delete=models.RESTRICT, limit_choices_to=Q(tabla__tabla='tipos_bono'), related_name='bonos_tipos', related_query_name='bono_tipo')

	class Meta:
		ordering = ['tipo', 'nombre']

	def get_absolute_url(self):
		return reverse('detalle_bono', kwargs={'pk':self.pk})

	def __str__(self):
		return self.nombre.upper()


# Tabla de Protagonistas
class Protagonista(SoftDeletionModel, TimestampsModel):
	""" Modelo Protagonista para el registro de las personas que reciben bonos de los proyectos. """

	cedula = models.CharField('Cédula', max_length=14, primary_key=True, help_text='Cédula de identidad sin guiones')
	nombres = models.CharField(max_length=100)
	apellidos = models.CharField(max_length=100)
	fecha_nacimiento = models.DateField('Fecha de nacimiento')
	sexo = models.CharField(max_length=1, choices=[('m', 'Masculino'), ('f', 'Femenino')])
	etnia = models.ForeignKey(DetalleTabla, on_delete=models.RESTRICT, limit_choices_to=Q(tabla__tabla='etnias'))
	comunidad = models.ForeignKey(Comunidad, on_delete=models.PROTECT)
	telefono = models.CharField('Teléfono', max_length=9, help_text='8888-8888', null=True, blank=True)
	promotor = models.BooleanField('Es Promotor', default=False)
	jvc = models.BooleanField('Miembro de JVC', default=False)

	def __str__(self):
		return "{0} {1}".format(self.nombres.upper(), self.apellidos.upper())

	def get_absolute_url(self):
		return reverse('detalle_protagonista', kwargs={'pk':self.pk})

	class Meta:
		ordering = ['apellidos', 'nombres']



# Tabla de Protagonistas con Bonos/Planes de inversión
class ProtagonistaBono(TimestampsModel, models.Model):
	""" 
	Modelo ProtagonistaBono para registro de los Bonos/Planes de inversión
	entregados a protagonistas.
	""" 

	protagonista = models.ForeignKey(Protagonista, on_delete=models.PROTECT)
	bono = models.ForeignKey(Bono, on_delete=models.PROTECT)
	proyecto = models.ForeignKey(Proyecto, on_delete=models.PROTECT)
	fecha_recibido = models.DateField(help_text='Fecha en que recibió el Bono/Plan de inversión.')
	tecnico = models.ForeignKey(Contacto, on_delete=models.RESTRICT, help_text='Técnico que realizó la entrega.', null=True)
	comunidad = models.ForeignKey(Comunidad, on_delete=models.PROTECT, help_text='Comunidad donde se ejecuta.')
	coord_x = models.FloatField('Coordenada UTM-X')
	coord_y = models.FloatField('Coordenada UTM-Y')
	altura = models.FloatField()
	observaciones = models.CharField(max_length=500, blank=True, null=True)
	digitador = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	activo = models.BooleanField(default=True, help_text='Está activo para seguimiento.')


	def __str__(self):
		return "{0} {1}>>{2}>>{3}".format(self.protagonista.nombres.upper(), self.protagonista.apellidos.upper(), self.bono.codigo.upper(), self.fecha_recibido)


	def get_absolute_url(self):
		return reverse('detalle_protagonista_bono', kwargs={'pk':self.pk})


	class Meta:
		ordering = ['protagonista','-fecha_recibido','bono']
		verbose_name = 'Protagonista con Bono/Plan'
		verbose_name_plural = 'Protagonistas con Bonos/Planes'


# Tabla de Capitalizacion
class CapitalizacionPlan(TimestampsModel):
	"""
	Modelo CapitalizacionBono para registrar la capitalización de los planes de inversión
	entregados a protagonistas.
	""" 

	protagonista_bono = models.ForeignKey(ProtagonistaBono, on_delete=models.CASCADE, limit_choices_to=Q(bono__tipo__elemento='plan_inversion'))
	articulo = models.ForeignKey(DetalleTabla, on_delete=models.RESTRICT, limit_choices_to=Q(tabla__tabla='articulos'), related_name='capitalizaciones_articulos', related_query_name='capitalizacion_articulo')
	unidad = models.ForeignKey(DetalleTabla, on_delete=models.RESTRICT, limit_choices_to=Q(tabla__tabla='unidades'), related_name='capitalizaciones_unidades', related_query_name='capitalizacion_unidad', help_text='Unidad de Medida')
	cantidad = models.IntegerField()
	costo = models.DecimalField('Costo unitario', max_digits=8, decimal_places=2, help_text='Costo en Córdobas(C$)')

	class Meta:
		ordering = ['protagonista_bono']




































from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from .managers import UserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date

TYPE_USER =(('1','STANDARD'),('2','SUSCRITO'),('3','PROFESIONAL'))

STATE_USER =(('1','ACTIVO'),('2','INACTIVO'),('3','BLOQUEADO'))

# Create your models here.
class User(AbstractBaseUser,PermissionsMixin):
    username = models.CharField(max_length=20,unique=True)
    first_name = models.CharField(max_length=10,blank=False,null=False)
    last_name = models.CharField(max_length=10,blank=False,null=False)
    age = models.CharField(max_length=2,blank=False)
    province = models.CharField(max_length=15,blank=False)
    country = models.CharField(max_length=15,blank=False)
    about_me = models.TextField()
    type_user = models.CharField(choices=TYPE_USER,max_length=20)
    state_user = models.CharField(choices=STATE_USER,max_length=20)
    email = models.EmailField(unique=True,blank=False,null=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','first_name','last_name']

    objects = UserManager()

    def get_short_name(self):
        return self.username
    
    def get_full_name(self):
        return self.first_name + self.last_name
    

class Suscription(models.Model):
    date_pay = models.DateField(auto_now=False, auto_now_add=False)
    type_suscription = models.CharField(max_length=50)
    concept = models.CharField(max_length=15,blank=False)
    amount = models.CharField(max_length=15,blank=False)
    type_pay = models.CharField(max_length=15,blank=False)
    valid_since = models.DateField(auto_now=False, auto_now_add=False)
    validity_until = models.DateField(auto_now=False, auto_now_add=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE)


class Profesional(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    dni = models.CharField(max_length=10)
    licencia = models.CharField(max_length=20)
    fecha_emision_licencia = models.DateField()
    titulo = models.CharField(max_length=100)
    e_provincia = models.CharField(max_length=15)
    e_pais = models.CharField(max_length=15)
    validacion = models.BooleanField(default=False)

    def __str__(self):
        return self.usuario.username

        # crear una receta nutritiva para el paciente
    def crear_receta(self, paciente, nombre_receta, ingredientes, instrucciones):
        receta = Receta.objects.create(profesional=self, paciente=paciente, nombre=nombre_receta, ingredientes=ingredientes, instrucciones=instrucciones)
        return receta

        # retorna la lista de pacientes asignados a este profesional
    def pacientes_asignados(self):
        return Paciente.objects.filter(profesional=self)

@receiver(post_save, sender=User)
def update_profesional(sender, instance, **kwargs):
    if instance.type_user == '3' and not hasattr(instance, 'profesional'):
        fecha_manual = date(2023, 5, 31)
        Profesional.objects.create(usuario=instance, dni='', licencia='',
                                     fecha_emision_licencia=fecha_manual, titulo='',
                                     e_provincia='', e_pais='', validacion=False)
    elif instance.type_user != '3' and hasattr(instance, 'profesional'):
        instance.profesional.delete()

class PublicacionReceta(models.Model):
    titulo = models.CharField(max_length=100)
    contenido = models.TextField()
    fecha_publicacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo
    
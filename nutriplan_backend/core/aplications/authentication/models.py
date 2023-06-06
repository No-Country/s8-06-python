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


class Professional(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dni = models.CharField(max_length=10)
    medical_license = models.CharField(max_length=20)
    license_issue_date = models.DateField()
    title = models.CharField(max_length=100)
    province = models.CharField(max_length=15)
    country = models.CharField(max_length=15)
    validation_status = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


# Actualiza el usuario a professional creando nuevas validaciones 
# y solicita nuevos campos de validacion
@receiver(post_save, sender=User)
def update_professional(sender, instance, **kwargs):
    if instance.type_user != 'PROFESIONAL':
        if instance.type_user == 'STANDARD':
            instance.additional_field = models.CharField(max_length=100, blank=True)
            instance.save()
        instance.type_user = 'PROFESIONAL'
        instance.save()
    
    if not hasattr(instance, 'professional'):
        manual_date = date(2023, 5, 31)
        Professional.objects.create(
            user=instance,
            dni='',
            medical_license='',
            license_issue_date=manual_date,
            title='',
            province='',
            country='',
            validation_status=False
        )
    elif instance.type_user != 'PROFESIONAL' and hasattr(instance, 'professional'):
        instance.professional.delete()



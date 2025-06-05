from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from association.models import Association

class Role(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'roles'

class User(AbstractUser):
    password = models.CharField(max_length=128, null=True, blank=True)
    email = models.EmailField(max_length=242,unique=True)
    email_verified_at = models.DateTimeField(null=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    avatar_file = models.ImageField(upload_to='users/img/') # Carpeta donde se guardan las users/imágenes/
    volunteer_number = models.CharField(max_length=50, null=True, blank=True)
    association = models.ForeignKey(Association, null=True, blank=True, on_delete=models.SET_NULL)  # <-- Añadido
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        username = self.username if self.username else "No User"
        role_name = self.role.name if self.role else "No Role"
        return f"{username} - {role_name}"
    
    class Meta:
        db_table = 'users'

class Member(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    association = models.ForeignKey(Association, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)
    
    class Meta:
        db_table = 'members'
        unique_together = ['user', 'association']

class Observation(models.Model):
    cat = models.ForeignKey('cats.Cat', on_delete=models.CASCADE)
    observation = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Observation for {self.cat.name}"
    
    class Meta:
        db_table = 'observations'

@receiver(post_migrate)
def create_default_roles(sender, **kwargs):
    _ = kwargs  # Mark kwargs as used to avoid unused variable warning
    if sender.name == 'users':
        Role.objects.get_or_create(name='member')
        Role.objects.get_or_create(name='manager')

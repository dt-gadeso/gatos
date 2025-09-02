from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_migrate
from django.dispatch import receiver

class Role(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'roles'

class Association(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=242, unique=True, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    logo_file = models.ImageField(upload_to='association/img/', null=True, blank=True)
    location = models.ForeignKey('colonies.Location', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'associations'

class User(AbstractUser):
    password = models.CharField(max_length=128, null=True, blank=True)
    email = models.EmailField(max_length=242, unique=True)
    email_verified_at = models.DateTimeField(null=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    carnet_gatos = models.ImageField(upload_to='users/img/', null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    association = models.ForeignKey(Association, null=True, blank=True, on_delete=models.SET_NULL)
    casa_acogida = models.BooleanField(default=False)
    tiene_relevo = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)
    es_capturador = models.BooleanField(default=False)
    es_free = models.BooleanField(default=False)
    tiene_trampa = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        username = self.username if self.username else "No User"
        role_name = self.role.name if self.role else "No Role"
        return f"{username} - {role_name}"
    
    class Meta:
        db_table = 'users'

class User_Role(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.role.name}"
    
    class Meta:
        db_table = 'user_roles'
        unique_together = ['user', 'role']

class Member(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    association = models.ForeignKey(Association, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)
    
    class Meta:
        db_table = 'members'
        unique_together = ['user']

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

class Manager(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    association = models.ForeignKey(Association, on_delete=models.CASCADE, related_name='association_managers', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'managers'
        unique_together = ['user']




@receiver(post_migrate)
def create_default_roles(sender, **kwargs):
    _ = kwargs
    if sender.name == 'users':
        Role.objects.get_or_create(name='miembro')
        Role.objects.get_or_create(name='presidente/a')

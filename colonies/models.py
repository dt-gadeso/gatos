from django.db import models
from users.models import Manager

class Municipality(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'municipalities'
        verbose_name_plural = 'municipalities'

class Location(models.Model):
    address = models.CharField(max_length=255)
    municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.address}, {self.municipality.name}"
    
    class Meta:
        db_table = 'locations'

class Colony(models.Model):
    name = models.CharField(max_length=100)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    manager = models.ForeignKey('users.Manager', on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'colonies'
        verbose_name_plural = 'colonies'

class Council(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    emergency_email = models.EmailField()
    emergency_phone = models.CharField(max_length=15)
    logo_file = models.ImageField(upload_to='municipality/img/') 
    location = models.ForeignKey('colonies.Location', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'councils'

class Zone(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'zones'
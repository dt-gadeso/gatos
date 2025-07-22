from django.db import models
from users.models import Manager

class Municipality(models.Model):
    name = models.CharField(max_length=100)
    zone_id = models.ForeignKey('colonies.Zone', on_delete=models.SET_NULL, null=True, blank=True)
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

class Zone(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'zones'

class Incident(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    reported_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)
    resolution = models.TextField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    colony = models.ForeignKey('Colony', on_delete=models.CASCADE, related_name='incidents')

    def __str__(self):
        return f"{self.title} - {'Resuelta' if self.is_resolved else 'Pendiente'}"
    
    class Meta:
        db_table = 'incidents'
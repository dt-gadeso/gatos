from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
# from users.models import User  # REMOVE
from municipality.models import Location
from association.models import Manager

class Colony(models.Model):
    name = models.CharField(max_length=100)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    manager = models.ForeignKey(Manager, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'colonies'
        verbose_name_plural = 'colonies'
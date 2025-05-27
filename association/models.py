from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal


class Association(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'associations'

class Manager(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    association = models.ForeignKey(Association, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'managers'
        unique_together = ['user', 'association']
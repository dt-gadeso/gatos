from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
# from users.models import User  # REMOVE
# from colonies.models import Colony  # REMOVE

class Cat(models.Model):
    SEX_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    
    name = models.CharField(max_length=50)
    photo_file = models.CharField(max_length=255, null=True, blank=True)
    chip = models.CharField(max_length=50, unique=True, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    sterilized = models.BooleanField(default=False)
    dead = models.BooleanField(default=False)
    colony = models.ForeignKey('colonies.Colony', on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'cats'
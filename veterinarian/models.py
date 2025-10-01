from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
from colonies.models import Municipality, Location
from users.models import Manager


class VetCenter(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    logo_file = models.ImageField(upload_to='veterinarian/img/', blank=True, null=True)
    location = models.ForeignKey('colonies.Location', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'vet_centers'


class Visit(models.Model):
    colony = models.ForeignKey('colonies.Colony', on_delete=models.CASCADE, null=True, blank=True)
    colony_user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='colony_user', null=True, blank=True)
    cat = models.ForeignKey('cats.Cat', on_delete=models.CASCADE, null=True, blank=True)
    vet_center = models.ForeignKey(VetCenter, on_delete=models.CASCADE, null=True, blank=True)
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    report_file = models.FileField(upload_to='veterinarian/field/visit', blank=True, null=True) 
    bill_file = models.FileField(upload_to='veterinarian/field/visit', blank=True, null=True) 
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    follow_up = models.TextField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    cat_survived = models.BooleanField(default=True, verbose_name="¿El gato sobrevivió?")
    returned_to_colony = models.BooleanField(default=False, null=True, blank=True, verbose_name="¿Ha vuelto a la colonia?")
    HOUSING_CHOICES = [
        ('none', 'Ninguno'),
        ('foster', 'Casa de acogida'),
        ('adoption', 'Adopción')
    ]
    housing_type = models.CharField(max_length=10, choices=HOUSING_CHOICES, default='none', null=True, blank=True, verbose_name="Tipo de alojamiento")
    housing_address = models.TextField(blank=True, null=True, verbose_name="Dirección de acogida/adopción")
    adoption_file = models.FileField(upload_to='veterinarian/field/adoption', blank=True, null=True, verbose_name="Archivo de adopción")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Visit for {self.cat.name} at {self.vet_center.name}"
    
    class Meta:
        db_table = 'visits'
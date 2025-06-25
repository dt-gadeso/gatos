from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
from colonies.models import Municipality, Location, Council
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

class Agreement(models.Model):
    council = models.ForeignKey('colonies.Council', on_delete=models.CASCADE)
    vet_center = models.ForeignKey(VetCenter, on_delete=models.CASCADE)
    week_days = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(7)]
    )
    week_cats = models.IntegerField(validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'agreements'

class VetService(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'vet_services'

class Visit(models.Model):
    cat = models.ForeignKey('cats.Cat', on_delete=models.CASCADE)
    vet_center = models.ForeignKey(VetCenter, on_delete=models.CASCADE)
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    report_file = models.CharField(max_length=255)
    bill_file = models.CharField(max_length=255)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    visit_date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Visit for {self.cat.name} at {self.vet_center.name}"
    
    class Meta:
        db_table = 'visits'

class VisitService(models.Model):
    visit = models.ForeignKey(Visit, on_delete=models.CASCADE)
    vet_service = models.ForeignKey(VetService, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'visit_services'
        unique_together = ['visit', 'vet_service']

class AgreementService(models.Model):
    agreement = models.ForeignKey('Agreement', on_delete=models.CASCADE)
    vet_service = models.ForeignKey('VetService', on_delete=models.CASCADE)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'agreement_services'
        unique_together = ['agreement', 'vet_service']
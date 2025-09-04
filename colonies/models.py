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
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    users_colony = models.TextField(null=True, blank=True)
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
    class IncidentType(models.TextChoices):
        URGENCY = 'URG', 'Urgencia'
        VANDALISM = 'VAN', 'Vandalismo'
        NEIGHBOR_CONFLICT = 'CON', 'Conflicto vecinal'
        ILLNESS = 'ENF', 'Enfermedad'
        ABANDONMENT = 'ABD', 'Abandono'
        BIRTH = 'PAR', 'Parto'
        CER = 'CER', 'CER'

    title = models.CharField(max_length=200)
    incident_type = models.CharField(
        max_length=3,
        choices=IncidentType.choices,
        default=IncidentType.URGENCY
    )
    description = models.TextField()
    reported_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)
    resolution = models.TextField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    colony = models.ForeignKey('Colony', on_delete=models.CASCADE, related_name='incidents')
    cat = models.ForeignKey('cats.Cat', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {'Resuelta' if self.is_resolved else 'Pendiente'}"
    
    class Meta:
        db_table = 'incidents'

class Relief(models.Model):
    class AlertType(models.TextChoices):
        RELIEF_NEEDED = 'REL', 'Necesidad de relevo'
        CLEANING_NEEDED = 'LIM', 'Necesidad de limpieza'
        SHELTER_NEEDED = 'REF', 'Necesidad de refugios'
        SOLIDARITY_NETWORK = 'SOL', 'Red Solidaria'

    title = models.CharField(max_length=200)
    alert_type = models.CharField(
        max_length=3,
        choices=AlertType.choices,
        default=AlertType.RELIEF_NEEDED
    )
    description = models.TextField()
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} - {self.get_alert_type_display()}"
    
    class Meta:
        db_table = 'relief'
        verbose_name = 'Aviso'
        verbose_name_plural = 'Avisos'

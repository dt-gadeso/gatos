from django.db import models


class Cat(models.Model):
    SEX_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    
    STATUS_CHOICES = [
        ('V', 'Vivo'),
        ('E', 'Enfermo'),
        ('M', 'Muerto'),
    ]
    
    catname = models.CharField(max_length=50)
    photo_file = models.ImageField(upload_to='cats/img/') # Carpeta donde se guardan las cats/imágenes/
    chip = models.CharField(max_length=50, unique=True, null=False)
    birthday = models.DateField(null=False)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    sterilized = models.BooleanField(default=False)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='V', verbose_name="Estado del gato")
    colony = models.ForeignKey('colonies.Colony', on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def status_display(self):
        return dict(self.STATUS_CHOICES)[self.status]
    
    @property
    def dead(self):
        # Para mantener compatibilidad con el código antiguo
        return self.status == 'M'
    
    def __str__(self):
        return self.catname
    
    class Meta:
        db_table = 'cats'

from django.db import models


class Cat(models.Model):
    SEX_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    
    catname = models.CharField(max_length=50)
    photo_file = models.ImageField(upload_to='cats/img/') # Carpeta donde se guardan las cats/imágenes/
    chip = models.CharField(max_length=50, unique=True, null=False)
    birthday = models.DateField(null=False)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    sterilized = models.BooleanField(default=False)
    dead = models.BooleanField(default=False)
    colony = models.ForeignKey('colonies.Colony', on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.catname
    
    class Meta:
        db_table = 'cats'

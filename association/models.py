from django.db import models


class Association(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=242,unique=True,  null=True, blank=True)  
    phone = models.CharField(max_length=20,  null=True, blank=True)   
    logo_file = models.ImageField(upload_to='association/img/', null=True, blank=True)
    location = models.ForeignKey('municipality.Location', on_delete=models.CASCADE, null=True, blank=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'associations'

class Manager(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)  # Use string reference
    association = models.ForeignKey(Association, on_delete=models.CASCADE, related_name='association_managers', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'managers'
        unique_together = ['user', 'association']
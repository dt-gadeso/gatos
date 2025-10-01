from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('veterinarian', '0013_visit_colony_visit_colony_user_visit_housing_address_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='visit',
            name='adoption_file',
            field=models.FileField(upload_to='veterinarian/field/adoption', blank=True, null=True, verbose_name='Archivo de adopción'),
        ),
    ]

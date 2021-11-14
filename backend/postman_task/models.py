from django.db import models

# Create your models here.

class Image(models.Model):
    id = models.AutoField(primary_key=True)
    image_file = models.ImageField(upload_to='images', blank= True, null= True)
    image_url = models.TextField(blank= True, null = True)
    widht = models.IntegerField(blank=True, null = True)
    height = models.IntegerField(blank=True, null = True)


    class Meta:
        managed = True
        db_table = 'images'
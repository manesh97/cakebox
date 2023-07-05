from django.db import models

# Create your models here.
class Cakes(models.Model):
    name=models.CharField(max_length=250)
    flavour=models.CharField(max_length=200)
    price=models.FloatField()
    shape=models.CharField(max_length=230)
    weight=models.CharField(max_length=250)
    layer=models.CharField(max_length=200)
    pic=models.ImageField(upload_to="images",null=True,blank=True)

    def __str__(self):
        return self.name

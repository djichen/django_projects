from django.db import models

# Create your models here.
class Category(models.Model) :
    name = models.CharField(max_length=128)

    def __str__(self) :
        return self.name

class States(models.Model) :
    name = models.CharField(max_length=128)

    def __str__(self) :
        return self.name

class Region(models.Model) :
    name = models.CharField(max_length=128)

    def __str__(self) :
        return self.name

class Iso(models.Model) :
    name = models.CharField(max_length=128)

    def __str__(self) :
        return self.name



class Site(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=128, null=True)
    justification = models.CharField(max_length=128, null=True)
    year = models.IntegerField(null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    states = models.ForeignKey(States, on_delete=models.CASCADE, null=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, null = True)
    iso = models.ForeignKey(Iso, on_delete=models.CASCADE, null=True)
    area_hectares = models.FloatField(null=True, blank=True, default=None)
    latitude = models.FloatField(null=True, blank=True, default=None)
    longitude = models.FloatField(null=True, blank=True, default=None)


    def __str__(self) :
        return self.name
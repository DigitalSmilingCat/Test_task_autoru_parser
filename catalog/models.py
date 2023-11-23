from django.db import models


class CarBrand(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f'{self.name}'


class CarModel(models.Model):
    name = models.CharField(max_length=255)

    brand = models.ForeignKey(CarBrand, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'

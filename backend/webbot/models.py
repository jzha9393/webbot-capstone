from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Product(models.Model):
    name = models.CharField(max_length=120)
    brand = models.CharField(max_length=120, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    reviewNumber = models.IntegerField(default=0)
    category = models.TextField(max_length=999, blank=True, null=True)

    sku = models.CharField(max_length=65, blank=True, null=True)
    upc = models.CharField(max_length=65, blank=True, null=True)
    ean = models.CharField(max_length=65, blank=True, null=True)
    mpn = models.CharField(max_length=65, blank=True, null=True)


class Review(models.Model):
    user = models.CharField(max_length=120, default='anonymous')
    date = models.DateField(blank=True, null = True)
    platform = models.CharField(max_length=120)
    title = models.CharField(max_length=120)
    text = models.TextField()
    rating = models.FloatField(
        validators=[MinValueValidator(0.0),
                    MaxValueValidator(5.0)])

    # foreign key
    product = models.ForeignKey('Product', on_delete=models.CASCADE)  # one to many

from django.db import models


class Product(models.Model):
    productname = models.CharField(max_length=100)
    productquantity = models.CharField(max_length=100)
    productstock = models.IntegerField()
    productprice = models.FloatField(max_length=100)
    productimage = models.ImageField()

    def __str__(self):
        return self.productname

from django.db import models


class Product(models.Model):
    productname = models.CharField(max_length=100)
    productquantity = models.IntegerField()
    productstock = models.CharField(max_length=100)
    productprice = models.FloatField(max_length=100)

    def __str__(self):
        return self.productname

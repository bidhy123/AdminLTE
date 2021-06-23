from django.db import models


class Category(models.Model):
    categoryname = models.CharField(max_length=100)
    vendor = models.CharField(max_length=100)

    def __str__(self):
        return self.categoryname

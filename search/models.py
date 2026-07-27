from django.db import models

# Create your models here.

class Produit(models.Model):
  ingredient = models.CharField(max_length=200)



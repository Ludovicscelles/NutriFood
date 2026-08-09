# import the necessary modules
# settings.py file is used to configure the Django project settings
from django.conf import settings
# models.py file is used to define the database models for the application
from django.db import models

# Create your models here.

# The Produit model represents a product in the database. 
# It has fields for the product name, ingredients, nutriscore, and category. 
# The nutriscore field is a choice field that allows users to select a value from a predefined list of options.
class Produit(models.Model):
  NUTRISCORE_CHOICES = [
    ("A", "A"),
    ("B", "B"),
    ("C", "C"),
    ("D", "D"),
    ("E", "E")
  ]

  code = models.CharField(
    max_length=50,
    unique=True,
  )

  nom = models.CharField(
     max_length=200,
     default="Produit inconnu",
     )

  marque = models.CharField(
    max_length=200,
    blank=True,
  )
  
  ingredients = models.TextField(blank=True)

  nutriscore = models.CharField(
    max_length=1,
    choices=NUTRISCORE_CHOICES,
    default="E",
  )
  categorie = models.CharField(
     max_length=200, 
     blank=True,
  )

  # The __str__ method is a special method in Python that returns a string representation of an object.
  def __str__(self):
    return self.nom


# The Remplacement model represents a replacement product in the database.
# It has fields for the user who created the replacement, the original product, the replacement product, and the date the replacement was created.
class Remplacement(models.Model):
  utilisateur = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
  )
  produit_original = models.ForeignKey(
    Produit,
    on_delete=models.CASCADE,
    related_name="remplacements_originaux"
  )
  produit_remplacement = models.ForeignKey(
    Produit,
    on_delete=models.CASCADE,
    related_name="remplacements_proposes"
  )
  date_creation = models.DateTimeField(auto_now_add=True)

  def __str__(self):
      return (
        f"{self.produit_original} -> "
        f"{self.produit_remplacement}"
      )
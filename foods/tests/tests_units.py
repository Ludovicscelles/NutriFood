from django.test import SimpleTestCase

from search.models import Produit
from search.views import est_meilleur_nutriscore


class NutriscoreTests(SimpleTestCase):

  def test_alternative_meilleure(self):
    produit = Produit(nutriscore="D")
    alternative = Produit(nutriscore="B")

    resultat = est_meilleur_nutriscore(
      alternative,
      produit
    )

    self.assertTrue(resultat)


  def test_alternative_moins_bonne(self):
    produit = Produit(nutriscore="C")
    alternative = Produit(nutriscore="E")

    resultat = est_meilleur_nutriscore(
      alternative,
      produit
    )

    self.assertFalse(resultat)


  def test_alternative_meme_nutriscore(self):
    produit = Produit(nutriscore="B")
    alternative = Produit(nutriscore="B")

    resultat = est_meilleur_nutriscore(
      alternative,
      produit
    )

    self.assertFalse(resultat)
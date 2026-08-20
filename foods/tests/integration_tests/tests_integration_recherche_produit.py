from django.test import TestCase
from django.urls import reverse

from search.models import Produit


class RechercheProduitTest(TestCase):

  def test_recherche_retourne_produit_correspondant(self):
    produit = Produit.objects.create(
      code="1234567890123",
      nom="Céréales chocolatées",
      marque="La Fabrique à Céréales",
      ingredients="Céréales, sucre, chocolat",
      nutriscore="D",
      categorie="Petit-déjeuner",
    )

    response = self.client.get(
      reverse('search:recherche_produit'),
      {"q": "Céréales chocolatées"}
    )

    self.assertEqual(response.status_code, 200)

    self.assertTemplateUsed(
      response,
      "search/resultats.html"
    )

    self.assertIn(

      produit,
      response.context["produits"]
    )


from django.test import TestCase
from django.urls import reverse

from search.models import Produit

class RechercheProduitDetail(TestCase):

  def setUp(self):
    self.produit = Produit.objects.create(
      code="123467890123",
      nom="Céréales chocolatées",
      marque="La Fabrique à Céréales",
      ingredients="Céréales, sucre, chocolat",
      nutriscore="D",
      categorie="Petit-déjeuner"
    )

  def test_detail_produit_existant(self):

    response = self.client.get(
      reverse(
        "search:produit_detail",
        args=[self.produit.code]
      )
    )

    self.assertEqual(response.status_code, 200)

    self.assertTemplateUsed(
      response,
      "search/produit_detail.html"
    )

    self.assertEqual(
      self.produit,
      response.context["article"]
    )

  def test_detail_produit_inexistant(self):

    response = self.client.get(
      reverse(
        "search:produit_detail",
        args=["9999999999999999"]
      )
     )

    self.assertEqual(
      response.status_code,
      404
    )
    
# import the necessary modules for testing
from django.test import TestCase
from django.urls import reverse

from search.models import Produit

# Create your tests here.


class AlternativeProduitTests(TestCase):

  # Test that the alternative view returns the correct context data when a product with a better nutriscore is found
  def test_alternative_avec_meilleur_nutriscore(self):
    produit = Produit.objects.create(
      nom="Céréales chocolatées",
      marque="Marque A",
      code="1234567890123",
      nutriscore="D",
    )

    meilleur_produit = Produit.objects.create(
      nom="Céréales chocolatées allégées",
      marque="Marque B",
      code="9876543210987",
      nutriscore="B",
    )

    Produit.objects.create(
      nom="Céréales chocolatées sucrées",
      marque="Marque C",
      code="4567890123456",
      nutriscore="E",
    )

    response = self.client.get(
      reverse("search:alternative"),
      {"q": "Céréales chocolatées"},
    )

    self.assertEqual(response.status_code, 200)

    self.assertTemplateUsed(
      response,
      "search/alternative.html"
    )

    self.assertEqual(
      response.context["produit"],
      produit
    )

    self.assertEqual(
      response.context["alternative"],
      meilleur_produit
    )

  def test_aucune_alternative_disponible(self):
    produit = Produit.objects.create(
      nom="Chips nature",
      marque="Marque D",
      code="1111111111111",
      nutriscore="C",
      )

    response = self.client.get(
      reverse("search:alternative"),
      {"q": "Chips nature"},
    )

    self.assertEqual(response.status_code, 200)

    self.assertTemplateUsed(
      response,
      "search/alternative.html"
    )

    self.assertEqual(
      response.context["produit"],
      produit
    )

    self.assertIsNone(
      response.context["alternative"]
    )

    # other way to check if the alternative is None
    # self.assertEqual(
    #   response.context["alternative"],
    #   None
    # )

  def test_produit_inexistant(self):
    response = self.client.get(
      reverse("search:alternative"),
      {"q": "Produit inexistant"},
    )

    self.assertEqual(response.status_code, 200)

    self.assertTemplateUsed(
      response,
      "search/alternative.html"
    )

    self.assertIsNone(
      response.context["produit"]
    )

    self.assertIsNone(
      response.context["alternative"]
    )

  def test_aucune_alternative_si_produit_est_meilleur(self):
    produit = Produit.objects.create(
      nom="Boisson sucrée",
      marque="Marque E",
      code="2222222222222",
      nutriscore="C",
    )

    Produit.objects.create(
      nom="Boisson sucrée light",
      marque="Marque F",
      code="3333333333333",
      nutriscore="D",
    )

    response = self.client.get(
      reverse("search:alternative"),
      {"q": "Boisson sucrée"},
    )

    self.assertEqual(response.status_code, 200)

    self.assertTemplateUsed(
      response,
      "search/alternative.html"
    )

    self.assertEqual(
      response.context["produit"],
      produit
    )

    self.assertIsNone(
      response.context["alternative"]
    )
from django.test import TestCase
from django.urls import reverse

from search.models import Produit


class RechercheProduitTest(TestCase):

  def setUp(self):
    self.produit = Produit.objects.create(
      code="1234567890123",
      nom="Céréales chocolatées",
      marque="La Fabrique à Céréales",
      ingredients="Céréales, sucre, chocolat",
      nutriscore="D",
      categorie="Petit-déjeuner",
    )

  def test_recherche_retourne_produit_correspondant(self):
   
    response = self.client.get(
    reverse("search:recherche_produit"),
    {"q": "Céréales chocolatées"}
    )

    self.assertEqual(response.status_code, 200)

    self.assertTemplateUsed(
      response,
      "search/resultats.html"
    )

    self.assertIn(
      self.produit,
      response.context["produits"]
    )

  def test_recherche_insensible_a_la_casse(self):
    
    response = self.client.get(
      reverse("search:recherche_produit"),
      {"q": "CéRéALeS"},
    )

    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(
      response,
      "search/resultats.html"
    )

    self.assertIn(
      self.produit,
      response.context["produits"]
    )

  def test_recherche_vide_ne_retourne_aucun_produit(self):

    response = self.client.get(
      reverse("search:recherche_produit"),
      {"q": ""},
    )

    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(
        response,
        "search/resultats.html"
    )

    self.assertEqual(
      response.context["produits"].count(),
      0
    )

    # other way to test the function :

    # self.assertNotIn(
    #   self.produit,
    #   response.context["produits"]
    # )

    
  def test_recherche_ignore_espaces_avant_apres(self):

    response = self.client.get(
      reverse("search:recherche_produit"),
      {"q": " Céréales Chocolatées "}
    )

    self.assertEqual(response.status_code, 200)

    self.assertTemplateUsed(
      response,
      "search/resultats.html"
    )

    self.assertIn(
      self.produit,
      response.context["produits"]
    )

    self.assertEqual(
      response.context["query"],
      "Céréales Chocolatées"
    )


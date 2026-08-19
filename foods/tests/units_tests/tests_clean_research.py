from django.test import SimpleTestCase

from search.views import nettoyer_recherche

class NettoyerRechercheTest(SimpleTestCase):

  def test_supprime_espace_avant_apres(self):
    resultat = nettoyer_recherche(" céréales ")

    self.assertEqual(resultat, "céréales")


  def test_sans_espace_reste_identique(self):
    resultat = nettoyer_recherche("Coca-Cola")

    self.assertEqual(resultat, "Coca-Cola")

  def test_uniquement_espaces_devient_vide(self):
    resultat = nettoyer_recherche("       ")

    self.assertEqual(resultat, "")

  def test_chaine_vide_reste_vide(self):
    resultat = nettoyer_recherche("")

    self.assertEqual(resultat, "")

    

    
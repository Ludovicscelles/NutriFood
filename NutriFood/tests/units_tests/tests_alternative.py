from unittest.mock import Mock

from django.test import SimpleTestCase

from search.views import alternative_valide


class AlternativeValideTests(SimpleTestCase):

  def test_alternative_meilleur(self):
    produit = Mock(nutriscore="D")
    alternative = Mock(nutriscore="B")

    self.assertTrue(alternative_valide(produit, alternative))

    # other way to test the function :
    # self.assertEqual(alternative_valide(produit, alternative), True)

  def test_alternative_moins_bonne(self):
    produit = Mock(nutriscore="B")
    alternative = Mock(nutriscore="E")

    self.assertFalse(alternative_valide(produit, alternative))

    # other way to test the function :
    # self.assertEqual(alternative_valide(produit, alternative), False)

  def test_alternative_identique(self):
    produit = Mock(nutriscore="B")
    alternative = Mock(nutriscore="B")

    self.assertFalse(alternative_valide(produit, alternative))


  def test_alternative_none(self):
    produit = Mock(nutriscore="B")

    self.assertFalse(alternative_valide(produit, None))
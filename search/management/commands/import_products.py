import requests

from django.core.management.base import BaseCommand, CommandError
from search.models import Produit

class Command(BaseCommand):
  help = "Importe les produits depuis l'API Open Food Facts dans la base de données"

  def handle(self, *args, **options):
    # Define the URL for the Open Food Facts API endpoint to retrieve products.
    url = "https://world.openfoodfacts.org/api/v2/search"

    # Define a list of required categories to filter the products retrieved from the API.
    required_categories = [
      "en:milk-chocolates",
      "en:dark-chocolates",
      "en:white-chocolates",
      "en:chocolate-spreads",
      "en:chocolate-biscuits",
    ]

    # Define the fields to retrieve from the API for each product.
    fields = (
      "code,product_name_fr,product_name,brands,"
      "ingredients_text,ingredients_text_fr,"
      "nutriscore_grade,categories_tags"
    )

    # Define headers for the API request to specify the user agent and accept JSON responses.
    headers = {
      "User-Agent": "NutriFood/1.0",
      "Accept": "application/json",
    }

    created_count = 0
    updated_count = 0 
    ignored_count = 0

    for category in required_categories:
      self.stdout.write(
        f"\nRécupération des produits pour la catégorie : {category}"
      )

      # Define parameters for the API request, including the category, page number, page size, language, and fields to retrieve.
      params = {
        "categories_tags": category,
        "page": 1,
        "page_size": 100,
        "lc": "fr",
        "fields": fields,
      }

      self.stdout.write("Récupération des données en cours ...")

      try:
        response = requests.get(
          url, 
          params=params,
          headers=headers,
          timeout=120,
        )
        response.raise_for_status()
        data = response.json()

      except requests.RequestException as error:
        self.stdout.write(
          self.style.ERROR(
            f"Impossible de récupérer les données de la catégorie {category} : {error}"
          )
        )
        continue

      except ValueError as error:
        self.stdout.write(  
          self.style.ERROR(
            f"Erreur lors de la conversion du JSON pour la catégorie {category} : {error}"
          )
        )
        continue

      products = data.get("products", [])

      for product in products:

        created = self.save_product(product)

        if created is True:
          created_count += 1
        elif created is False:
          updated_count += 1
        else:
          ignored_count += 1

    self.stdout.write(
      self.style.SUCCESS(
        "Importation terminée : "
        f"{created_count} produits créés, "
        f"{updated_count} produits mis à jour, "
        f"{ignored_count} produits ignorés."
      )
    )

  def save_product(self, product):

    code = product.get("code")

    if not code:
      return None

    nom = (
      product.get("product_name_fr") 
      or product.get("product_name") 
      or "Produit inconnu"
    )

    marque = product.get("brands") or "Marque inconnue"

    ingredients = (
      product.get("ingredients_text_fr") 
      or product.get("ingredients_text") 
      or ""
    )

    grade = product.get("nutriscore_grade")

    if grade in {"a", "b", "c", "d", "e"}:
      grade = grade.upper() 
    else:
      grade = "E"

    categories = product.get("categories_tags") or []
    categorie = ", ".join(categories)[:200]

    produit_db, created = Produit.objects.update_or_create(
      code=code,
      defaults={
        "nom": nom[:200],
        "marque": marque[:200],
        "ingredients": ingredients,
        "nutriscore": grade,
        "categorie": categorie,
      },
    )

    return created
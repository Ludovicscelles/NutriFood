import requests

# Django imports to handle management commands
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):

  help = "Met à jour la base de données depuis l'API Open Food Facts"

  # This method is called when the command is executed
  def handle(self, *args, **options):

    # define variables for the API request, categories and fields to retrieve.

    url = "https://world.openfoodfacts.org/api/v2/search"

    required_categories = [
      "en:milk-chocolates",
      "en:dark-chocolates",
      "en:white-chocolates",
      "en:chocolate-spreads",
      "en:chocolate-biscuits",
    ]

    fields = (
      "code,product_name_fr,product_name,"
      "nutriscore_grade,countries_tags,brands,ingredients_text,ingredients_text_fr,"
      "ingredients,ingredients_analysis_tags,additives_tags,additives_n,additives,"
      "nutriments,allergens,allergens_tags,allergens_from_ingredients,"
      "allergens_from_user,labels,labels_tags,labels_hierarchy,"
      "categories,categories_tags,categories_hierarchy,"
      "traces,traces_tags,states,states_tags,states_hierarchy,"
      "manufacturing_places,manufacturing_places_tags,"
      "packaging,packaging_tags,packaging_text,packaging_text_fr,"
      "quantity,serving_size,serving_quantity,"
      "ingredients_from_palm_oil_n,ingredients_from_palm_oil_tags,"
    )

    # Define headers for the API request to specify the user agent and accept JSON responses.
    headers = {
      "User-Agent": "NutriFood/1.0",
      "Accept": "application/json",
    }

    # Initialize a dictionary to store products by their unique code to avoid duplicates.
    products_per_code = {}

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

      # Make the API request and handle potential errors, including network issues and invalid JSON responses.
      try: 
        response = requests.get(
          url,
          params=params, 
          timeout=120,
          headers=headers,
        )

        self.stdout.write(
          f"URL envoyée : {response.url}"
        )

        self.stdout.write(
          f"Réponse reçue : HTTP {response.status_code}"
        )
        self.stdout.write(f"Réponse : {response.text[:500]}")

        response.raise_for_status()

        self.stdout.write("Conversion du JSON...")

        # Retrieve the JSON data from the response and handle potential errors related to JSON decoding.
        data = response.json()

        self.stdout.write("JSON converti.")

      # Handle exceptions for request errors and JSON decoding errors, providing informative error messages to the user.
      except requests.RequestException as error:
        self.stdout.write(
          self.style.ERROR(
            f"Impossible de récupérer les données pour la catégorie {category}. "
            f"Erreur : {error}" 
          )
        )
        continue

      except ValueError as error:
        self.stdout.write(
          self.style.ERROR(
            f"JSON invalide reçu pour la catégorie {category}."
            f"Erreur : {error}"
          )
        )
        continue

      # Retrieve the list of products from the JSON data, limiting to the first 100 products for each category to avoid excessive data retrieval.
      products = data.get("products", [])[:100]

      self.stdout.write(
        self.style.SUCCESS(
          f"{len(products)} produit(s) récupéré(s) pour la catégorie {category}"
        )
      )

      # Store each product in the dictionary using its unique code as the key to ensure that only unique products are kept across all categories.
      for product in products:
          code = product.get("code")
          if code:
            products_per_code[code] = product

    products = list(products_per_code.values())

    self.stdout.write(
      self.style.SUCCESS(
        f"\n{len(products)} produit(s) uniques récupéré(s) pour les catégories : {', '.join(required_categories)}"
      )
    )


    # Display the retrieved products in a readable format, including their name, code, Nutri-Score, calories, ingredients, palm oil content, categories, and countries of origin.
    for count, product in enumerate(products, start=1):
      self.display_product(product, count)
      
      
    

  def display_product(self, product, count):

      
      nom = (
        product.get("product_name_fr")
        or product.get("product_name") 
        or "Nom inconnu"
      )

      code = product.get("code") or "Code inconnu"

      grade = product.get("nutriscore_grade")

      if grade in {"a", "b", "c", "d", "e"}:
        grade = grade.upper()
      else:
        grade = "Nutri-Score non renseigné"

      ingredients = (
        product.get("ingredients_text_fr") 
        or product.get("ingredients_text") 
        or "Ingrédients non renseignés"
      )

      oil_palm = product.get("ingredients_from_palm_oil_n")

      if oil_palm is None:
        oil_palm = "Non renseigné" 


      nutriments = product.get("nutriments") or {}

      calories = nutriments.get("energy-kcal_100g")

      if calories is None:
        calories_display = "Non renseigné"
      else:
        calories_display = f"{calories} kcal/100g"

      categories = product.get("categories_tags") or []

      countries = product.get("countries_tags") or []

      self.stdout.write(
        f"\nProduit {count} :"
        f"\n- {nom}"
        f"\n Code : {code}"
        f"\n Nutri-Score : {grade}"
        f"\n Calories : {calories_display}"
        f"\n Ingrédients : {ingredients}"
        f"\n Ingrédients contenant de l'huile de palme : {oil_palm}"
        f"\n Catégories : "
        f"{', '.join(categories) if categories else 'Non renseignées'} - "
        f"\n Pays : "
        f"{', '.join(countries) if countries else 'Non renseignés'}"
      )

      
import requests

from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):

  help = "Met à jour la base de données depuis l'API Open Food Facts"

  def handle(self, *args, **options):
    url = "https://world.openfoodfacts.org/api/v2/search"

    params = {
      "categories_tags": "en:chocolates",
      "page_size": 10,
      "lc": "fr",
      "fields": (
        "code,product_name_fr,product_name,"
        "nutriscore_grade"
      ),
    }

    self.stdout.write("Récupération des données en cours ...")

    try: 
      response = requests.get(
        url,
        params=params, 
        timeout=30,
        headers={
          "User-Agent": "NutriFood/1.0"
        }
      )
      response.raise_for_status()
      data = response.json()

    except requests.RequestException as error:
      raise CommandError(
        f"Impossible de récupérer les données : {error}"
      ) from error

    except ValueError as error:
      raise CommandError(
        "La réponse reçue n'est pas un JSON valide."
      ) from error

    produits = data.get("products", [])

    self.stdout.write(
      self.style.SUCCESS(
        f"{len(produits)} produit(s) récupéré(s)" 
      )
    )

    for produit in produits:
      nom = (
        produit.get("product_name_fr")
        or produit.get("product_name") 
        or "Nom inconnu"
      )

      code = produit.get("code") or "Code inconnu"

      grade = produit.get("nutriscore_grade")

      if grade in {"a", "b", "c", "d", "e"}:
        grade = grade.upper()
      else:
        grade = "Nutri-Score non renseigné"

      self.stdout.write(f"- {nom} - {code} - {grade}")
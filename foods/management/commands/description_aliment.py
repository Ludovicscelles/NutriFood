from django.core.management.base import BaseCommand

class Command(BaseCommand):

  help = "Affiche la description d'un aliment"

  def add_arguments(self, parser):
    parser.add_argument(
      "aliment",
      type=str,
      help="Nom de l'aliment à afficher",
    )

  def handle(self, *args, **options):
    aliment = options["aliment"]

    self.stdout.write(
      self.style.SUCCESS(
        f"Description de l'aliment sélectionné : {aliment}"
        )
    )
from django.core.management.base import BaseCommand

class Command(BaseCommand):

  help = "Affiche un message de bienvenue"

  def handle(self, *args, **options):
    self.stdout.write(
      self.style.SUCCESS("Bonjour depuis Django !")
    )
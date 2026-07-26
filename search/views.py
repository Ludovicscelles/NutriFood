from django.http import HttpResponse

# Create your views here.
def index(request):
  return HttpResponse("Hey ! tu es sur l'index de l'application search du projet NutriFood.")

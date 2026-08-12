# render is a function that takes a request object and a template name, 
# and returns an HttpResponse object with the rendered template.
from django.shortcuts import render
# import the Produit model from the models.py file in the same directory
from .models import Produit

# Create your views here.
# The index function is a view that renders the index.html template when the user visits the root URL of the application.
def index(request):
    return render(request, 'search/index.html')

# The recherche_produit function is a view that handles the search functionality for products.
def recherche_produit(request):
    # get the search query from the request object using the GET method
    query = request.GET.get('q')

    # filter the Produit objects based on the search query using the icontains lookup
    produits = Produit.objects.filter(
        nom__icontains=query
    )

    # render the resultats.html template with the filtered products as context
    return render(
        request, 
        'search/resultats.html', 
        {
            'query': query,
            'produits': produits
            },
    )
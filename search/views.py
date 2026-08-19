# render is a function that takes a request object and a template name, 
# and returns an HttpResponse object with the rendered template.
from django.shortcuts import render, get_object_or_404
# import the Produit model from the models.py file in the same directory
from .models import Produit

# Create your views here.
# The index function is a view that renders the index.html template when the user visits the root URL of the application.
def index(request):
    return render(request, 'search/index.html')


def nettoyer_recherche(query):
    return query.strip()

# The recherche_produit function is a view that handles the search functionality for products.
def recherche_produit(request):
    query = nettoyer_recherche(request.GET.get('q', ''))


    if query:
        # if the query is not empty, filter the Produit objects based on the search query using the icontains lookup
        produits = Produit.objects.filter(
            nom__icontains=query
        )
    else:
        # if the query is empty, return an empty queryset
        produits = Produit.objects.none()

    # render the resultats.html template with the filtered products as context
    return render(
        request, 
        'search/resultats.html', 
        {
            'query': query,
            'produits': produits
            },
    )

def produit_detail(request, barcode):
    # get the product object from the database using the barcode parameter passed in the URL
    # if the product does not exist, return a 404 error page
    produit = get_object_or_404(Produit, code=barcode)

    # render the produit_detail.html template with the product object as context
    return render (
        request,
        'search/produit_detail.html',
        {
            'article': produit
        }
    )


ORDRE_NUTRISCORE = {
    "A": 1,
    "B": 2,
    "C": 3,
    "D": 4,
    "E": 5,
}

def est_meilleur_nutriscore(alternative, produit):
    return ORDRE_NUTRISCORE[alternative.nutriscore] < ORDRE_NUTRISCORE[produit.nutriscore]

def alternative_valide(produit, alternative):
    if alternative is None:
        return False

    return est_meilleur_nutriscore(
        alternative,
        produit
    )

def alternative_produit(request):
    query = nettoyer_recherche(request.GET.get('q', ''))

    produit = None
    alternative = None

    if query:

        produit = Produit.objects.filter(
            nom__icontains=query
        ).first()
    
        if produit:
            alternative = Produit.objects.filter(
                nom__icontains=query
            ).exclude(
                id=produit.id
            ).order_by('nutriscore').first()

            if not alternative_valide(produit, alternative):
                alternative = None

    return render(
        request,
        'search/alternative.html',
        {
            'query': query,
            'produit': produit,
            'alternative': alternative,
        }
    )


    
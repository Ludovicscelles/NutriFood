from django.urls import path

from . import views

app_name = 'search'

urlpatterns = [
  path('', views.index, name='index'),
  path('recherche/', views.recherche_produit, name='recherche_produit'),
]

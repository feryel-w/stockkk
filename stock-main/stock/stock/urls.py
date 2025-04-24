
from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('admin/', admin.site.urls),
     # Clients
    path('clients/', views.liste_clients, name='liste_clients'),
    path('clients/ajouter/', views.ajouter_client, name='ajouter_client'),
    path('clients/modifier/<int:id>/', views.modifier_client, name='modifier_client'),
    path('clients/supprimer/<int:id>/', views.supprimer_client, name='supprimer_client'),

    # Fournisseurs
    path('fournisseurs/', views.liste_fournisseurs, name='liste_fournisseurs'),
    path('fournisseurs/ajouter/', views.ajouter_fournisseur, name='ajouter_fournisseur'),
    path('fournisseurs/modifier/<int:id>/', views.modifier_fournisseurs, name='modifier_fournisseur'),
    path('fournisseurs/supprimer/<int:id>/', views.supprimer_fournisseurs, name='supprimer_fournisseur'),

    # Catégories
    path('categories/', views.liste_categories, name='liste_categories'),
    path('categories/ajouter/', views.ajouter_categorie, name='ajouter_categorie'),
    path('categories/modifier/<int:id>/', views.modifier_categories, name='modifier_categorie'),
    path('categories/supprimer/<int:id>/', views.supprimer_categories, name='supprimer_categorie'),

    # Produits
    path('produits/', views.liste_produits, name='liste_produits'),
    path('produits/ajouter/', views.ajouter_produit, name='ajouter_produit'),
    path('produits/modifier/<int:id>/', views.modifier_produit, name='modifier_produit'),
    path('produits/supprimer/<int:id>/', views.supprimer_produit, name='supprimer_produit'),

    path('mouvements/ajouter/', views.ajouter_mouvement, name='ajouter_mouvement'),
    path('mouvements/', views.liste_mouvements, name='liste_mouvements'),

    path('caisse/', views.caisse_view, name='caisse'),

    path('dashboard/', views.dashboard, name='dashboard'),

    path('', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('envoyer-email/', views.send_email_view, name='envoyer_email'),


]

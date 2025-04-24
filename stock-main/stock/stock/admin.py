from django.contrib import admin
from .models import Categorie, Fournisseur, Produit , MouvementStock
from .models import Categorie, Fournisseur, Produit, Client, MouvementStock



@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom')
    search_fields = ('nom',)

@admin.register(Fournisseur)
class FournisseurAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'telephone', 'pays', 'gouvernorat' , 'email')
    search_fields = ('nom', 'email')
    def save_model(self, request, obj, form, change):
        obj.clean()
        obj.save()

@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'categorie', 'fournisseur', 'quantite_stock', 'prix_achat', 'prix_vente' )
    list_filter = ('categorie', 'fournisseur')
    search_fields = ('nom',)

from .models import Client

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'telephone', 'pays', 'gouvernorat' , 'email')
    search_fields = ('nom', 'email')
    def save_model(self, request, obj, form, change):
        obj.clean()
        obj.save()

@admin.register(MouvementStock)
class MouvementStockAdmin(admin.ModelAdmin):
    list_display = ('produit', 'type_mouvement', 'quantite', 'date_mouvement', 'client', 'gain', 'depense','revenu' , 'fournisseur')
    list_filter = ('type_mouvement', 'date_mouvement')
    
    



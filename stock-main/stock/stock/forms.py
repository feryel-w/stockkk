from django import forms
from .models import Client, Fournisseur, Categorie, Produit , MouvementStock


class MouvementStockForm(forms.ModelForm):
    class Meta:
        model = MouvementStock
        fields = ['produit', 'type_mouvement', 'quantite', 'client']
class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['nom', 'pays', 'gouvernorat', 'telephone', 'email']

class FournisseurForm(forms.ModelForm):
    class Meta:
        model = Fournisseur
        fields = ['nom', 'pays', 'gouvernorat', 'telephone', 'email']

class CategorieForm(forms.ModelForm):
    class Meta:
        model = Categorie
        fields = ['nom']

class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        fields = ['nom', 'description', 'quantite_stock', 'prix_achat', 'prix_vente' ,'categorie', 'fournisseur']

from django import forms
from .models import Client, Fournisseur

class EmailForm(forms.Form):
    recipients_choice = forms.ChoiceField(
        choices=[('clients', 'Clients'), ('fournisseurs', 'Fournisseurs')],
        widget=forms.RadioSelect,
        required=True
    )
    recipients = forms.ModelMultipleChoiceField(
        queryset=Client.objects.all(),  # Default to clients; this will change based on the form selection
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    subject = forms.CharField(max_length=255, required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        recipients_choice = self.initial.get('recipients_choice', 'clients')
        if recipients_choice == 'fournisseurs':
            self.fields['recipients'].queryset = Fournisseur.objects.all()

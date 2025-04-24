from django.shortcuts import render, redirect, get_object_or_404
from .models import Client, Fournisseur, Categorie, Produit, MouvementStock
from .forms import ClientForm, FournisseurForm, CategorieForm, ProduitForm
from django.db.models import Sum, Q
from .models import MouvementStock
from .forms import MouvementStockForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, redirect
from django.db.models.functions import TruncDate
from django.contrib.auth.decorators import login_required


@login_required
# ----------------- MOUVEMENTS DE STOCK -----------------
def ajouter_mouvement(request):
    form = MouvementStockForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('liste_mouvements')
    return render(request, 'stock/ajouter_mouvement.html', {'form': form})
@login_required
def liste_mouvements(request):
    query = request.GET.get('q')
    if query:
        mouvements = MouvementStock.objects.filter(
            Q(produit__nom__icontains=query) |
            Q(type_mouvement__icontains=query) |
            Q(client__nom__icontains=query) |
            Q(fournisseur__nom__icontains=query)
        )
    else:
        mouvements = MouvementStock.objects.all().order_by('-date_mouvement')
    return render(request, 'stock/liste_mouvements.html', {'mouvements': mouvements, 'query': query})


@login_required
# ----------------- PRODUITS -----------------
def ajouter_produit(request):
    form = ProduitForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('liste_produits')
    return render(request, 'stock/ajouter_produit.html', {'form': form})
@login_required
def liste_produits(request):
    query = request.GET.get('q')
    if query:
        produits = Produit.objects.filter(
            Q(nom__icontains=query) |
            Q(description__icontains=query) |
            Q(categorie__nom__icontains=query) |
            Q(fournisseur__nom__icontains=query)
        )
    else:
        produits = Produit.objects.all()
    return render(request, 'stock/liste_produits.html', {'produits': produits, 'query': query})
@login_required
def modifier_produit(request, id):
    produit = get_object_or_404(Produit, id=id)
    form = ProduitForm(request.POST or None, instance=produit)
    if form.is_valid():
        form.save()
        return redirect('liste_produits')
    return render(request, 'stock/modifier_produits.html', {'form': form})
@login_required
def supprimer_produit(request, id):
    produit = get_object_or_404(Produit, id=id)
    if request.method == 'POST':
        produit.delete()
        return redirect('liste_produits')
    return render(request, 'stock/supprimer_produit.html', {'produit': produit})
@login_required
# ----------------- CLIENTS -----------------
def ajouter_client(request):
    form = ClientForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('liste_clients')
    return render(request, 'stock/ajouter_client.html', {'form': form})
@login_required
def liste_clients(request):
    query = request.GET.get('q')
    if query:
        clients = Client.objects.filter(
            Q(nom__icontains=query) |
            Q(email__icontains=query) |
            Q(telephone__icontains=query)
        )
    else:
        clients = Client.objects.all()
    return render(request, 'stock/liste_clients.html', {'clients': clients, 'query': query})
@login_required
def modifier_client(request, id):
    client = get_object_or_404(Client, id=id)
    form = ClientForm(request.POST or None, instance=client)
    if form.is_valid():
        form.save()
        return redirect('liste_clients')
    return render(request, 'stock/modifier_client.html', {'form': form})
@login_required
def supprimer_client(request, id):
    client = get_object_or_404(Client, id=id)
    if request.method == 'POST':
        client.delete()
        return redirect('liste_clients')
    return render(request, 'stock/supprimer_client.html', {'client': client})
@login_required
# ----------------- FOURNISSEURS -----------------
def ajouter_fournisseur(request):
    form = FournisseurForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('liste_fournisseurs')
    return render(request, 'stock/ajouter_fournisseur.html', {'form': form})
@login_required
def liste_fournisseurs(request):
    query = request.GET.get('q')
    if query:
        fournisseurs = Fournisseur.objects.filter(
            Q(nom__icontains=query) |
            Q(email__icontains=query) |
            Q(telephone__icontains=query) |
            Q(pays__icontains=query) |
            Q(gouvernorat__icontains=query)
        )
    else:
        fournisseurs = Fournisseur.objects.all()
    return render(request, 'stock/liste_fournisseurs.html', {'fournisseurs': fournisseurs, 'query': query})
@login_required
def modifier_fournisseurs(request, id):
    fournisseur = get_object_or_404(Fournisseur, id=id)
    form = FournisseurForm(request.POST or None, instance=fournisseur)
    if form.is_valid():
        form.save()
        return redirect('liste_fournisseurs')
    return render(request, 'stock/modifier_fournisseurs.html', {'form': form})
@login_required
def supprimer_fournisseurs(request, id):
    fournisseur = get_object_or_404(Fournisseur, id=id)
    if request.method == 'POST':
        fournisseur.delete()
        return redirect('liste_fournisseurs')
    return render(request, 'stock/supprimer_fournisseurs.html', {'fournisseur': fournisseur})
@login_required
# ----------------- CATÉGORIES -----------------
def ajouter_categorie(request):
    form = CategorieForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('liste_categories')
    return render(request, 'stock/ajouter_categorie.html', {'form': form})
@login_required
def liste_categories(request):
    query = request.GET.get('q')
    if query:
        categories = Categorie.objects.filter(
            Q(nom__icontains=query)
        )
    else:
        categories = Categorie.objects.all()
    return render(request, 'stock/liste_categories.html', {'categories': categories, 'query': query})
@login_required
def modifier_categories(request, id):
    categorie = get_object_or_404(Categorie, id=id)
    form = CategorieForm(request.POST or None, instance=categorie)
    if form.is_valid():
        form.save()
        return redirect('liste_categories')
    return render(request, 'stock/modifier_categories.html', {'form': form})
@login_required
def supprimer_categories(request, id):
    categorie = get_object_or_404(Categorie, id=id)
    if request.method == 'POST':
        categorie.delete()
        return redirect('liste_categories')
    return render(request, 'stock/supprimer_categories.html', {'categorie': categorie})

# ----------------- DASHBOARD -----------------
#def dashboard(request):
    total_produits = Produit.objects.count()
    total_clients = Client.objects.count()
    total_fournisseurs = Fournisseur.objects.count()
    total_entrees = MouvementStock.objects.filter(type_mouvement='ENTREE').aggregate(Sum('quantite'))['quantite__sum'] or 0
    total_sorties = MouvementStock.objects.filter(type_mouvement='SORTIE').aggregate(Sum('quantite'))['quantite__sum'] or 0
    return render(request, 'stock/dashboard.html', {
        'total_produits': total_produits,
        'total_clients': total_clients,
        'total_fournisseurs': total_fournisseurs,
        'total_entrees': total_entrees,
        'total_sorties': total_sorties,
    })
    ''''
@login_required
def dashboard_mouvements(request): 
    total_mouvements = MouvementStock.objects.count()
    total_entrees = MouvementStock.objects.filter(type_mouvement='ENTREE').aggregate(Sum('quantite'))['quantite__sum'] or 0
    total_sorties = MouvementStock.objects.filter(type_mouvement='SORTIE').aggregate(Sum('quantite'))['quantite__sum'] or 0

    derniers_mouvements = MouvementStock.objects.order_by('-date_mouvement')[:5]

    produits_plus_sortis = (
        MouvementStock.objects
        .filter(type_mouvement='SORTIE')
        .values('produit__nom')
        .annotate(total_sortie=Sum('quantite'))
        .order_by('-total_sortie')[:5]
    )

    # Données pour graphique camembert
    total_entrees_chart = total_entrees
    total_sorties_chart = total_sorties

    # Données pour l'évolution dans le temps
    mouvements_par_jour = (
        MouvementStock.objects
        .annotate(jour=TruncDate('date_mouvement'))
        .values('jour', 'type_mouvement')
        .annotate(total=Sum('quantite'))
        .order_by('jour')
    )

    # Organiser les données
    dates = sorted(set(m['jour'] for m in mouvements_par_jour))
    entrees_par_jour = []
    sorties_par_jour = []

    for date in dates:
        total_entree = sum(m['total'] for m in mouvements_par_jour if m['jour'] == date and m['type_mouvement'] == 'ENTREE')
        total_sortie = sum(m['total'] for m in mouvements_par_jour if m['jour'] == date and m['type_mouvement'] == 'SORTIE')
        entrees_par_jour.append(total_entree)
        sorties_par_jour.append(total_sortie)

    # Données pour le graphique produits les plus sortis
    labels = [p['produit__nom'] for p in produits_plus_sortis]
    data = [p['total_sortie'] for p in produits_plus_sortis]

    # Context final
    context = {
        'total_mouvements': total_mouvements,
        'total_entrees': total_entrees,
        'total_sorties': total_sorties,
        'derniers_mouvements': derniers_mouvements,
        'produits_plus_sortis': produits_plus_sortis,
        'labels': labels,
        'data': data,
        'entree_sortie_labels': ['Entrées', 'Sorties'],
        'entree_sortie_data': [total_entrees_chart, total_sorties_chart],
        'dates': [d.strftime('%Y-%m-%d') for d in dates],
        'entrees_data': entrees_par_jour,
        'sorties_data': sorties_par_jour,
    }

    return render(request, 'stock/dashboard.html', context) 
    '''
def caisse_view(request):
    revenus_totaux = MouvementStock.objects.filter(type_mouvement='SORTIE').aggregate(Sum('revenu'))['revenu__sum'] or 0
    total_gain = MouvementStock.objects.aggregate(Sum('gain'))['gain__sum'] or 0
    total_depense = MouvementStock.objects.aggregate(Sum('depense'))['depense__sum'] or 0
    solde = total_gain - total_depense

    context = {
        'revenus_totaux': revenus_totaux,  # Retirer l'espace après 'revenu'
        'total_gain': total_gain,
        'total_depense': total_depense,
        'solde': solde,
    }
    return render(request, 'stock/caisse.html', context)

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'stock/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'stock/login.html', {'form': form})

from django.db.models import F


def dashboard(request):
    # Get recent stock movements (limit to 5 latest)
    recent_movements = MouvementStock.objects.order_by('-date_mouvement')[:5]

    # Calculate total movements
    total_movements = MouvementStock.objects.count()

    # Calculate total revenue (sum of 'revenu' for all SORTIE movements)
    total_revenue = MouvementStock.objects.filter(type_mouvement='SORTIE').aggregate(Sum('revenu'))['revenu__sum'] or 0

    # Calculate total expenses (sum of 'depense' for all ENTREE movements)
    total_expenses = MouvementStock.objects.filter(type_mouvement='ENTREE').aggregate(Sum('depense'))['depense__sum'] or 0

    # Calculate balance (revenue - expenses)
    total_balance = total_revenue - total_expenses

    # Get top sold products (most quantities sold, SORTIE only)
    top_sold_products = MouvementStock.objects.filter(type_mouvement='SORTIE').values('produit__nom').annotate(
        total_quantity=Sum('quantite')
    ).order_by('-total_quantity')[:5]

    # Get low stock products (stock level < reorder threshold)
    low_stock_products = Produit.objects.filter(quantite_stock__lte=10)

    # Count total 'ENTREE' and 'SORTIE' movements
    total_entree_count = MouvementStock.objects.filter(type_mouvement='ENTREE').count()
    total_sortie_count = MouvementStock.objects.filter(type_mouvement='SORTIE').count()

    # Total quantity moved per type
    total_entree_quantity = MouvementStock.objects.filter(type_mouvement='ENTREE').aggregate(
        Sum('quantite')
    )['quantite__sum'] or 0
    total_sortie_quantity = MouvementStock.objects.filter(type_mouvement='SORTIE').aggregate(
        Sum('quantite')
    )['quantite__sum'] or 0

    context = {
        'recent_movements': recent_movements,
        'total_movements': total_movements,
        'total_revenue': total_revenue,
        'total_expenses': total_expenses,
        'total_balance': total_balance,
        'top_sold_products': top_sold_products,
        'low_stock_products': low_stock_products,
        'total_entree_count': total_entree_count,
        'total_sortie_count': total_sortie_count,
        'total_entree_quantity': total_entree_quantity,
        'total_sortie_quantity': total_sortie_quantity,
    }

    return render(request, 'stock/dashboard.html', context)

from django.shortcuts import render
from .forms import EmailForm
from .models import Client, Fournisseur
from django.core.mail import send_mail

def send_email_view(request):
    msg = None
    recipients_data = []
    selected_type = request.GET.get('recipients_choice', 'client')  # default to client

    if selected_type == 'client':
        recipients_data = Client.objects.all()
    elif selected_type == 'fournisseur':
        recipients_data = Fournisseur.objects.all()

    if request.method == 'POST':
        form = EmailForm(request.POST)
        selected_type = request.POST.get('recipients_choice')
        selected_ids = request.POST.getlist('recipients')  # Get selected checkboxes

        if selected_type == 'client':
            selected_recipients = Client.objects.filter(id__in=selected_ids)
        else:
            selected_recipients = Fournisseur.objects.filter(id__in=selected_ids)

        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            recipient_emails = [r.email for r in selected_recipients]

            try:
                send_mail(
                    subject,
                    message,
                    'feryelturki9@gmail.com',  # sender
                    recipient_emails,
                    fail_silently=False,
                )
                msg = "Emails sent successfully!"
            except Exception as e:
                msg = f"An error occurred while sending emails: {str(e)}"
    else:
        form = EmailForm()

    return render(request, 'stock/email.html', {
        'form': form,
        'msg': msg,
        'recipients_data': recipients_data,
        'selected_type': selected_type,
    })

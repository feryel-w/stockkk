from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

PAYS_CHOICES = [
    ('Tunisie', 'Tunisie'),
    ('Algérie', 'Algérie'),
    ('Maroc', 'Maroc'),
    ('France', 'France'),
    ('Italie', 'Italie'),
    ('Autre', 'Autre'),
]
GOUVERNORAT_CHOICES = [
    ('Ariana', 'Ariana'),
    ('Béja', 'Béja'),
    ('Ben Arous', 'Ben Arous'),
    ('Bizerte', 'Bizerte'),
    ('Gabès', 'Gabès'),
    ('Gafsa', 'Gafsa'),
    ('Jendouba', 'Jendouba'),
    ('Kairouan', 'Kairouan'),
    ('Kasserine', 'Kasserine'),
    ('Kébili', 'Kébili'),
    ('Le Kef', 'Le Kef'),
    ('Mahdia', 'Mahdia'),
    ('La Manouba', 'La Manouba'),
    ('Médenine', 'Médenine'),
    ('Monastir', 'Monastir'),
    ('Nabeul', 'Nabeul'),
    ('Sfax', 'Sfax'),
    ('Sidi Bouzid', 'Sidi Bouzid'),
    ('Siliana', 'Siliana'),
    ('Sousse', 'Sousse'),
    ('Tataouine', 'Tataouine'),
    ('Tozeur', 'Tozeur'),
    ('Tunis', 'Tunis'),
    ('Zaghouan', 'Zaghouan'),
]
INDICATIF_PAYS = {
    'Tunisie': '+216',
    'Algérie': '+213',
    'Maroc': '+212',
    'France': '+33',
    'Italie': '+39',
}


class Categorie(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class Fournisseur(models.Model):
    nom = models.CharField(max_length=100)
    pays = models.CharField(max_length=50, choices=PAYS_CHOICES, default='Tunisie')
    gouvernorat = models.CharField(max_length=50, choices=GOUVERNORAT_CHOICES, blank=True)
    telephone = models.CharField(max_length=20)
    email = models.EmailField()

    def clean(self):
        indicatif = INDICATIF_PAYS.get(self.pays)

        # Si déjà formaté correctement
        if self.telephone.startswith(indicatif):
            return

        # Sinon, nettoyer et préfixer
        numero_sans_espace = self.telephone.replace(" ", "").replace("-", "")

        if not numero_sans_espace.isdigit():
            raise ValidationError("Le numéro doit contenir uniquement des chiffres.")

        longueur_attendue = 8 if self.pays == 'Tunisie' else 9
        if len(numero_sans_espace) != longueur_attendue:
            raise ValidationError(f"Le numéro doit contenir {longueur_attendue} chiffres pour {self.pays}.")

        self.telephone = indicatif + numero_sans_espace

    def __str__(self):
        return self.nom

class Produit(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    quantite_stock = models.IntegerField(default=0)
    prix_achat = models.DecimalField(max_digits=10, decimal_places=2)
    prix_vente = models.DecimalField(max_digits=10, decimal_places=2)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE)

    def __str__(self):
        return self.nom
    

class Client(models.Model):
    nom = models.CharField(max_length=100)
    pays = models.CharField(max_length=50, choices=PAYS_CHOICES, default='Tunisie')
    gouvernorat = models.CharField(max_length=50, choices=GOUVERNORAT_CHOICES, blank=True)
    telephone = models.CharField(max_length=20)
    email = models.EmailField()

    def clean(self):
        indicatif = INDICATIF_PAYS.get(self.pays)

        # Si déjà formaté correctement
        if self.telephone.startswith(indicatif):
            return

        # Sinon, nettoyer et préfixer
        numero_sans_espace = self.telephone.replace(" ", "").replace("-", "")

        if not numero_sans_espace.isdigit():
            raise ValidationError("Le numéro doit contenir uniquement des chiffres.")

        longueur_attendue = 8 if self.pays == 'Tunisie' else 9
        if len(numero_sans_espace) != longueur_attendue:
            raise ValidationError(f"Le numéro doit contenir {longueur_attendue} chiffres pour {self.pays}.")

        self.telephone = indicatif + numero_sans_espace

    def __str__(self):
        return self.nom

class MouvementStock(models.Model):
    TYPE_MOUVEMENT_CHOICES = [
        ('ENTREE', 'Entrée'),
        ('SORTIE', 'Sortie'),
    ]

    produit = models.ForeignKey('Produit', on_delete=models.CASCADE)
    type_mouvement = models.CharField(max_length=10, choices=TYPE_MOUVEMENT_CHOICES)
    quantite = models.PositiveIntegerField()
    date_mouvement = models.DateTimeField(default=timezone.now)
    client = models.ForeignKey('Client', on_delete=models.SET_NULL, null=True, blank=True)
    fournisseur = models.ForeignKey('Fournisseur', on_delete=models.SET_NULL, null=True, blank=True)

    # Champs ajoutés pour le gain et la dépense
    gain = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    depense = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    revenu = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    def clean(self):
        # Règles de validation intelligentes
        if self.type_mouvement == 'ENTREE' and not self.fournisseur:
            raise ValidationError("Une entrée doit être liée à un fournisseur.")
        if self.type_mouvement == 'SORTIE' and not self.client:
            raise ValidationError("Une sortie doit être liée à un client.")
        if self.type_mouvement == 'SORTIE' and self.quantite > self.produit.quantite_stock:
            raise ValidationError("Stock insuffisant pour cette sortie.")
    def save(self, *args, **kwargs):
        self.clean()  # appeler clean() avant de sauver

        # Mettre à jour le stock automatiquement
        if self.pk is None:  # uniquement à la création
            if self.type_mouvement == 'ENTREE':
                self.produit.quantite_stock += self.quantite
                self.depense = self.produit.prix_achat * self.quantite  # Calcul de la dépense
                self.gain = 0  # Pas de gain sur une entrée
                self.revenu = 0  # Pas de revenu sur une entrée
            elif self.type_mouvement == 'SORTIE':
                self.produit.quantite_stock -= self.quantite
                self.depense = 0  # Pas de dépense pour une sortie
                self.revenu = self.produit.prix_vente * self.quantite  # Revenu brut
                if self.produit.prix_vente and self.produit.prix_achat:
                    self.gain = (self.produit.prix_vente - self.produit.prix_achat) * self.quantite  # Gain net

            self.produit.save()

        super().save(*args, **kwargs)
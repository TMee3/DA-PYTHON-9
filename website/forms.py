from django import forms
from website import models


class TicketForm(forms.ModelForm):
    """
    Formulaire pour créer un ticket.
    """
    class Meta:
        model = models.Ticket  # Associe le formulaire au modèle Ticket
        fields = ['title', 'description', 'image']  # Spécifie les champs à inclure dans le formulaire
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control mx-auto w-50 mb-3'}),  # Ajoute des classes CSS au champ title
            'description': forms.Textarea(attrs={'class': 'form-control mx-auto w-50 mb-3'})  # Ajoute des classes CSS au champ description
        }


class ReviewForm(forms.ModelForm):
    """
    Formulaire pour créer une critique. 
    """
    class Meta:
        model = models.Review  # Associe le formulaire au modèle Review
        fields = ['headline', 'rating', 'body']  # Spécifie les champs à inclure dans le formulaire
        CHOICES = [('1', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5)]  # Définit les choix de notation disponibles
        widgets = {
            'headline': forms.TextInput(attrs={'class': 'form-control mx-auto w-50 mb-3'}),  # Ajoute des classes CSS au champ headline
            'rating': forms.RadioSelect(choices=CHOICES, attrs={'class': 'form-check-label mx-3 '
                                                                     'd-flex justify-content-center'}),  # Utilise des boutons radio pour le champ rating
            'body': forms.Textarea(attrs={'class': 'form-control mx-auto w-50 mb-3'})  # Ajoute des classes CSS au champ body
        }


class FollowUsersForm(forms.ModelForm):
    """
    Formulaire pour créer un abonnement.
    """
    class Meta:
        model = models.UserFollows  # Associe le formulaire au modèle UserFollows
        fields = ['followed_user']  # Spécifie les champs à inclure dans le formulaire

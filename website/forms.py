from django import forms
from website import models

class TicketForm(forms.ModelForm):
    """
    Formulaire pour créer un ticket.
    """
    class Meta:
        model = models.Ticket
        fields = ['title', 'description', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control mx-auto w-50 mb-3'}),
            'description': forms.Textarea(attrs={'class': 'form-control mx-auto w-50 mb-3'})
        }


class ReviewForm(forms.ModelForm):
    """
    Formulaire pour créer une critique.
    """
    class Meta:
        model = models.Review
        fields = ['headline', 'rating', 'body']
        CHOICES = [('1', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5)]
        widgets = {
            'headline': forms.TextInput(attrs={'class': 'form-control mx-auto w-50 mb-3'}),
            'rating': forms.RadioSelect(choices=CHOICES, attrs={'class': 'form-check-label mx-3 d-flex justify-content-center'}),
            'body': forms.Textarea(attrs={'class': 'form-control mx-auto w-50 mb-3'})
        }


class FollowUsersForm(forms.ModelForm):
    """
    Formulaire pour créer un abonnement.
    """
    class Meta:
        model = models.UserFollows
        fields = ['followed_user']

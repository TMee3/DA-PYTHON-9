from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models

class Ticket(models.Model):
    """
    Ticket model
    """
    # Gestionnaire d'objets par défaut
    objects = models.Manager()

    # Titre du ticket
    title = models.CharField(max_length=128, db_index=True)
    # Description du ticket
    description = models.TextField(max_length=2048, blank=True)
    # Utilisateur associé au ticket
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # Image du ticket
    image = models.ImageField(null=True, blank=True)
    # Date de création du ticket
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Review(models.Model):
    """
    Review model
    """
    # Gestionnaire d'objets par défaut
    objects = models.Manager()

    # Ticket associé à la revue
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    # Évaluation de la revue avec des validateurs min/max
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    # Titre de la revue
    headline = models.CharField(max_length=128)
    # Corps de la revue
    body = models.TextField(max_length=8192, blank=True)
    # Utilisateur associé à la revue
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # Date de création de la revue
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.headline

class UserFollows(models.Model):
    # Gestionnaire d'objets par défaut
    objects = models.Manager()

    # Utilisateur qui suit
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='following_users')
    # Utilisateur suivi
    followed_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='followed_by')

    class Meta:
        # Assure qu'on n'obtient pas plusieurs instances de UserFollows pour les paires utilisateur-utilisateur_suivi uniques
        unique_together = ('user', 'followed_user')

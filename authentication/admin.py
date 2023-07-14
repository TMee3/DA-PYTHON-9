from django.contrib import admin
from .models import User

# Classe d'administration pour l'utilisateur
class UserAdmin(admin.ModelAdmin):
    # date_hierarchy = 'publication_date'  # Exemple d'option pour hiérarchie de dates
    list_display = ('username', 'email', 'is_superuser', 'is_staff', 'is_active')  # Colonnes à afficher dans la liste
    list_filter = ('is_superuser', 'is_active')  # Filtres à afficher dans la barre latérale

# Enregistrement du modèle utilisateur dans l'administration avec la classe d'administration correspondante
admin.site.register(User, UserAdmin)

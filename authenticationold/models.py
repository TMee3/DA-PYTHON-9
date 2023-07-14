from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Modèle d'utilisateur personnalisé étendant la classe AbstractUser de Django.
    Vous pouvez ajouter des champs supplémentaires ou personnaliser le comportement de l'utilisateur ici.

    Utilise le modèle de base de données par défaut, mais vous pouvez changer cela en définissant la variable 'objects'.
    """

    pass

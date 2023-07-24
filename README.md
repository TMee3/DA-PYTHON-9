# OCR_projet_9
## Description du projet:
  Ce projet s'inscrit dans le cadre de la formation "Développeur d'application : Python" d'OpenClassrooms. L'objectif de ce projet est de créer une MVP (Minimum Viable Product) pour une application permettant à une communauté d'utilisateurs de consulter ou de solliciter des critiques de livres à la demande.
  
## Fonctionnalités du programme:
  Ce programme offre les fonctionnalités suivantes :

Authentification et inscription : Les utilisateurs peuvent se connecter ou s'inscrire pour accéder à l'application.
Accès restreint : Le site n'est accessible qu'aux utilisateurs connectés.
Consultation du flux : Les utilisateurs peuvent consulter un flux contenant les derniers tickets et les commentaires des utilisateurs qu'ils suivent, classés par ordre chronologique (les plus récents en premier).
Création de critiques : Les utilisateurs peuvent créer des critiques en réponse à des tickets ou créer des critiques indépendantes. Dans le cadre d'un processus en une étape, l'utilisateur peut créer un ticket puis ajouter un commentaire en réponse à son propre ticket.
Gestion des tickets et commentaires : Les utilisateurs peuvent voir, modifier et supprimer leurs propres tickets et commentaires.
Suivi des utilisateurs : Les utilisateurs peuvent suivre d'autres utilisateurs en entrant leur nom d'utilisateur. Ils peuvent également voir la liste des utilisateurs qu'ils suivent et suivre/désuivre d'autres utilisateurs.

    
## Pré-requis:
   - Language de programmation:
      Python3
   - Module utilisés:
      - Django 4
   - Poetry
   
## Installation:
Clonez le dépôt du projet :
git clone <lien-du-depot>
cd OCR_projet_9

Installez Poetry (si vous ne l'avez pas déjà installé) :
curl -sSL https://install.python-poetry.org | python3 -

Installez les dépendances du projet en utilisant Poetry :
poetry install


## Utilisation:
Activez l'environnement virtuel créé par Poetry :
poetry shell

Exécutez le programme en utilisant Poetry :
python manage.py runserver

Dans votre navigateur internet, accédez au site en vous rendant à l'adresse http://127.0.0.1:8000/.
Une fois que le serveur local est en cours d'exécution et que vous accédez au site, vous pouvez commencer à utiliser les fonctionnalités de l'application de critique de livres. Assurez-vous de vous inscrire ou de vous connecter pour accéder à l'ensemble des fonctionnalités offertes par l'application.
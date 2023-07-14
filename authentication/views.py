from django.contrib.auth import login, authenticate, logout
from django.conf import settings
from django.shortcuts import render, redirect

from . import forms

# Page de connexion
def login_page(request):
    logout_user(request)  # Déconnexion de l'utilisateur avant d'afficher la page de connexion
    form = forms.LoginForm()
    message = ''
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)  # Connexion de l'utilisateur
                return redirect('flux')
            else:
                message = 'Identifiants invalides.'
    return render(request, 'authentication/login.html', context={'form': form, 'message': message})


# Déconnexion de l'utilisateur
def logout_user(request):
    logout(request)  # Déconnexion de l'utilisateur
    return redirect('login')


# Page d'inscription
def signup_page(request):
    form = forms.SignupForm()
    if request.method == "POST":
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()  # Sauvegarde de l'utilisateur
            login(request, user)  # Connexion de l'utilisateur
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, 'authentication/signup.html', context={'form': form})

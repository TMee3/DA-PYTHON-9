from django.contrib.auth import login, authenticate, logout
from django.conf import settings
from django.shortcuts import render, redirect

from . import forms

def login_page(request):
    logout(request)
    form = forms.LoginForm()
    message = ''

    if request.method == 'POST':
        form = forms.LoginForm(request.POST)

        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )

            if user is not None:
                login(request, user)
                return redirect('flux')
            else:
                message = 'Identifiants invalides.'

    context = {'form': form, 'message': message, 'errors': form.errors}
    return render(request, 'authentication/login.html', context=context)

def logout_user(request):
    logout(request)
    return redirect('login')

def signup_page(request):
    form = forms.SignupForm()

    if request.method == "POST":
        form = forms.SignupForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)

    context = {'form': form}
    return render(request, 'authentication/signup.html', context=context)

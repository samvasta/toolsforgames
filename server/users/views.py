from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm

def home(request):
    return render(request, 'users/home.html')

def register(request):
    if request.method == 'GET':
        form = UserRegisterForm()

    elif request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account successfully created for {username}. You may now log in.')
            return redirect('login')

    return render(request, 'users/register.html', {'form': form})

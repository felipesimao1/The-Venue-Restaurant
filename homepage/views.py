from collections import UserDict
from imaplib import _Authenticator
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
# Create your views here.

def homepage(request):
    return render(request, 'homepage.html')

def aboutus(request):
    return render(request, 'aboutus.html')

def menu(request):
    return render(request, 'menu.html')

def contact(request):
    return render(request, 'contact.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Check if user exists
        user = _Authenticator(username=username, password=password)
        if user is not None:
            login(request, user)
            print('User logged in')
            return redirect('home')
        else:
            print('User not found')
            return redirect('home')

    return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(username=username).exists():
                print('Username already exists')
                return redirect('signup')
            else:
                if User.objects.filter(email=email).exists():
                    print('Email already exists')
                    return redirect('signup')
                else:
                    user = User.objects.create_user(username=username, email=email, password=password)
                    user.save()
                    print('User created')
                    return redirect('homepage') #login
        else:
            print('Passwords do not match')
            return redirect('login')

    return render(request, 'signup.html')

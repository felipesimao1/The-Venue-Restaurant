import time
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import logout as django_logout
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Reservation


# Create your views here.

def homepage(request):
    return render(request, 'homepage.html')

def aboutus(request):
    return render(request, 'aboutus.html')

def menu(request):
    return render(request, 'menu.html')

def contact(request):
    return render(request, 'contact.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('homepage')
        else:
            return render(request, 'login.html', {'error_message': 'Invalid credentials'})
    return render(request, 'login.html')

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password == password2:
            if User.objects.filter(username=username).exists():
                return render(request, 'signup.html', {'error_message': 'Username already exists'})
            elif User.objects.filter(email=email).exists():
                return render(request, 'signup.html', {'error_message': 'Email already exists'})
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                login(request, user)
                return redirect('homepage')
        else:
            return render(request, 'signup.html', {'error_message': 'Passwords do not match'})

    return render(request, 'signup.html')

@login_required
def logout(request):
    django_logout(request)
    return render(request, 'homepage.html')

@login_required
def make_reservation(request):
    if request.method == 'POST':
        # Receber os dados do formulário
        date = request.POST.get('date')
        table = request.POST.get('table')
        time = request.POST.get('time')
        guests = request.POST.get('guests')

        # Criar uma nova reserva associada ao usuário atual
        reservation = Reservation.objects.create(date=date, table=table, time=time, guests=guests, user=request.user)

        # Redirecionar para a página de sucesso ou para a mesma página com uma mensagem de sucesso
        return redirect('make_reservation')  # ou ajuste conforme necessário
    else:
        # Obter todas as reservas existentes
        reservations = Reservation.objects.filter(user=request.user).order_by('date')
        return render(request, 'make_reservation.html', {'reservations': reservations})

@login_required
def edit_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)

    if request.method == 'POST':
        # Receber os dados do formulário
        reservation.date = request.POST.get('date')
        reservation.table = request.POST.get('table')
        reservation.time = request.POST.get('time')
        reservation.guests = request.POST.get('guests')
        reservation.save()
        return redirect('make_reservation')  # ou redirecione para onde desejar após a edição
    else:
        return render(request, 'editreservation.html', {'reservation': reservation})

@login_required
def delete_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    reservation.delete()
    return redirect('make_reservation')  # ou ajuste conforme necessário
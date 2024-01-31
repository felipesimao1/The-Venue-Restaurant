from datetime import date
from datetime import datetime
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import logout as django_logout
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Client, Reservation
from django.contrib import messages


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
            messages.success(request, 'Login Successful')
            return redirect('homepage')
        else:
            messages.error(request, 'Username or password is incorrect')
            return render(request, 'login.html', {'error_message': 'Invalid credentials'})
        
    return render(request, 'login.html')

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        # Verificar se as senhas coincidem
        if password != password2:
            # Se as senhas não coincidirem, você pode retornar uma mensagem de erro
            messages.error(request, 'Passwords do not match')
            return render(request, 'signup.html',)

        # Verificar se o usuário já existe
        if User.objects.filter(username=username).exists():
            # Se o usuário já existe, você pode retornar uma mensagem de erro
            messages.error(request, 'Username already exists')
            return render(request, 'signup.html')

        # Criar um novo usuário
        user = User.objects.create_user(username=username, email=email, password=password)

        # Você pode fazer mais aqui, como redirecionar para a página de login ou página inicial
        messages.success(request, 'Account created successfully')
        return redirect('login')
    
    return render(request, 'signup.html')
    
@login_required
def logout(request):
    django_logout(request)
    return render(request, 'homepage.html')

@login_required
def make_reservation(request):
    if request.method == 'POST':
        # Receber os dados do formulário
        date_str = request.POST.get('date')
        table = request.POST.get('table')
        time = request.POST.get('time')
        guests = request.POST.get('guests')

        # Converter a data do formato de string para objeto date
        reservation_date = datetime.strptime(date_str, '%Y-%m-%d').date()

        # Verificar se a data da reserva é no futuro
        current_date = date.today()
        
        if reservation_date < current_date:
            # Se a data da reserva for no passado, exibir uma mensagem de erro
            messages.error(request, 'A data da reserva não pode ser no passado. Por favor, escolha uma data futura.')
            return redirect('make_reservation')

        # Verificar se já existe uma reserva para a mesma data e hora
        existing_reservation = Reservation.objects.filter(date=date_str, time=time).exists()

        if existing_reservation:
            # Se uma reserva já existir para a mesma data e hora, exibir uma mensagem de erro
            messages.error(request, 'Já existe uma reserva para esta data e hora. Por favor, escolha outra data ou hora.')
            return redirect('make_reservation')
        else:
            # Criar uma nova reserva associada ao usuário atual
            reservation = Reservation.objects.create(date=date_str, table=table, time=time, guests=guests, user=request.user)
            
            # Redirecionar para a página de sucesso ou para a mesma página com uma mensagem de sucesso
            messages.success(request, 'Sua reserva foi feita com sucesso!')
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
        messages.success(request, 'Your reservation has been updated successfully!')
        return redirect('make_reservation')  # ou redirecione para onde desejar após a edição
    else:
        return render(request, 'editreservation.html', {'reservation': reservation})

@login_required
def delete_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    reservation.delete()
    messages.success(request, 'Your reservation has been deleted successfully!')
    return redirect('make_reservation')  # ou ajuste conforme necessário
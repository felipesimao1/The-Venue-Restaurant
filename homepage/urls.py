from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('about/', views.aboutus, name='aboutus'), 
    path('menu', views.menu, name='menu'),
    path('contact/', views.contact, name='contact'),
]

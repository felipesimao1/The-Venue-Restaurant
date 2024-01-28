from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('about/', views.aboutus, name='aboutus'), 
    path('menu', views.menu, name='menu'),
    path('contact/', views.contact, name='contact'),

    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout, name='logout'),

    path('reservation/', views.make_reservation, name='make_reservation'),
    path('reservation/<int:reservation_id>/edit/', views.edit_reservation, name='edit_reservation'),
    path('reservation/<int:reservation_id>/delete/', views.delete_reservation, name='delete_reservation'),
]

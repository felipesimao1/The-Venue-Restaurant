from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Client(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username
    
class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    table = models.IntegerField(default=1)
    guests = models.IntegerField()

    def __str__(self):
        return self.user.username + ' ' + str(self.date) + ' ' + str(self.time) + ' ' + str(self.guests)
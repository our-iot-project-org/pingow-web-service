from django.db import models

# Create your models here.

class UserProfile(models.Model):
    user_name = models.CharField(max_lenght=30)
    first_name = models.CharField(max_lenght=30)
    last_name = models.CharField(max_lenght=30)

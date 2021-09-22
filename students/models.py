from django.db import models
from django.contrib.auth.models import User
from courses.models import Subject

# Create your models here.
class Instructor(models.Model):
    username = models.OneToOneField(User,on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=14)
    dob = models.DateField(null=False)
    address = models.CharField(max_length=100)
    bio = models.TextField()

    def __str__(self):
        return str(self.username)

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg',upload_to='profile_pic')
    is_email_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} Profile'
    
    



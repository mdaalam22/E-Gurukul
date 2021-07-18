from django.db import models
from django.contrib.auth.models import User
from courses.models import Course

# Create your models here.

class Message(models.Model):
    course_name = models.ForeignKey(Course,on_delete=models.CASCADE)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.username

    def last_10_messages():
        return Message.objects.order_by('-timestamp').all()[:10]

    

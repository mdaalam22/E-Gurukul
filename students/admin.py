from django.contrib import admin
from .models import Instructor,Profile
from django.urls import reverse
from django.utils.safestring import mark_safe
from .views import *

def generate_report(obj):
    url = reverse('admin_generate_report', args=[obj.user.username])
    return mark_safe(f'<a href="{url}">Generate Report</a>')



@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ['username','phone_number','dob','address']
    list_filter = ['username']
    search_fields = ['username']

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'image', 'is_email_confirmed',generate_report]
    list_filter = ['user','is_email_confirmed']
    search_fields = ['user']

    
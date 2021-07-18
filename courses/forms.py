from django import forms
from django.forms.models import inlineformset_factory
from .models import Course, Module,Contact
from django.core import validators
import re

ModuleFormSet = inlineformset_factory(Course,Module,
                     fields=['title','description'],extra=2,can_delete=True)

def check_phone(value):
    if not bool(re.search('^[9][0-9]{9}$',value)):
        raise forms.ValidationError('Enter Valid phone number')
                  

class ContactForm(forms.Form):
    class Meta:
        fields = ('name','email','subject','phone_number','message')
        model = Contact
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Full Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Email Address'}))
    subject = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Subject'}))
    phone_number = forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'Phone Number'}),
                    validators=[check_phone,])
    message = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','placeholder':'Type your message here..'}))
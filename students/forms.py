from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from courses.models import Course
from .models import Instructor,Profile
from django.core import validators
import re
from django.contrib.auth.password_validation import UserAttributeSimilarityValidator,CommonPasswordValidator,MinimumLengthValidator,NumericPasswordValidator

# class InstructorForm(forms.Form):
#     class Meta:
#         model = Instructor
#         fields = ['username','phone_number','age','address',' subject_category','bio']
#     username =  forms.CharField(widget = forms.HiddenInput(attrs={'id':'usernameVal',}))
#     phone_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Phone Number',
#                                                                 'class':'form-control',}))
#     age = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder':'Your age',
#                                                                 'class':'form-control',}))
#     address = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Address',
#                                                                 'class':'form-control',}))
#     subject_category = forms.CharField(widget=forms.Select(attrs={'class':'form-control',}))
#     bio = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control',}))
def check_email(email):
    if User.objects.filter(email=email).exists():
        raise forms.ValidationError('Email Already Exist.Please try different email')

def check_phone(phone):
    if not bool(re.search('^[9][0-9]{9}$',phone)):
        raise forms.ValidationError('Please enter a valid phone number')



class CourseEnrollForm(forms.Form):
    course = forms.ModelChoiceField(queryset=Course.objects.all(),widget=forms.HiddenInput)


class SignUpForm(UserCreationForm):
    class Meta:
        fields = ('username','first_name', 'last_name', 'email','password1', 'password2')
        model = User
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username',
                                                                'class': 'form-control',
                                                                }))    
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First Name',
                                                                'class': 'form-control',
                                                                }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last Name',
                                                                'class': 'form-control',
                                                                }))
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Email',
                                                                'class': 'form-control mb-4',
                                                                }),validators=[check_email,])
    
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                'class': 'form-control mb-4',
                                                                }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password',
                                                                'class': 'form-control mb-4',
                                                                }))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password2'].label = "Confirm Password"



class StudentUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username',
                                                                'class': 'form-control',
                                                                }))    
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First Name',
                                                                'class': 'form-control',
                                                                }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last Name',
                                                                'class': 'form-control',
                                                                }))
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Email',
                                                                'class': 'form-control mb-4',}))

    # def clean_email(self):
    #     if not self.request.user.is_authenticated():
    #         if User.objects.filter(email=self.email).exist():
    #             raise forms.ValidationError('Email Already Exist. Please try different email')

# def psw_validate(password):
#     if len(password) < 8:
#         raise forms.ValidationError('Password mu')
# class ChangePasswordForm(forms.Form):
#     class Meta:
#         model =  User
#         fields = ['password1','password2']

#     password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password',
#                                                                 'class': 'form-control mb-4',
#                                                                 }),validators=[UserAttributeSimilarityValidator,CommonPasswordValidator,MinimumLengthValidator,NumericPasswordValidator])
#     password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password',
#                                                                 'class': 'form-control mb-4',
#                                                                 }))

class InstructorUpdateForm(forms.ModelForm):
    class Meta:
        model = Instructor
        fields = ['phone_number','dob','address','bio']

    phone_number = forms.CharField(widget=forms.NumberInput(attrs={'placeholder':'Phone Number',
                                                        'class':'form-control'}),validators=[check_phone,])
    dob = forms.DateField(widget=forms.DateInput(attrs={'type':'date','class':'form-control'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Address','class':'form-control'}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Write about yourself..',
                                                    'class':'form-control'}))

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
    
    image = forms.ImageField()
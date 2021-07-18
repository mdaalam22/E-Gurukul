from django.urls import reverse_lazy
from django.shortcuts import render,redirect
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from .forms import SignUpForm,CourseEnrollForm,ProfileUpdateForm,StudentUpdateForm,InstructorUpdateForm
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from courses.models import Course,Subject
from django.views.generic.detail import DetailView
from django.contrib.auth.models import User,Group
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import re
from django.views import View
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .models import Instructor
from django.core.mail import EmailMessage
from django.urls import reverse

from django.utils.encoding import force_bytes,force_text,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from .utils import token_generator
import threading
# Create your views here.


class EmailThread(threading.Thread):
	def __init__(self,email):
		self.email = email
		threading.Thread.__init__(self)

	def run(self):
		self.email.send(fail_silently=False)

class StudentRegistrationView(CreateView):
    template_name = 'students/student/registration.html'
    form_class = SignUpForm
    success_url = reverse_lazy('student_course_list')

    def form_valid(self, form):
        result = super().form_valid(form)
        cd = form.cleaned_data
       
        user = authenticate(username=cd['username'],password=cd['password1'])
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        domain = get_current_site(self.request).domain
        link = reverse('activate',
                    kwargs={'uidb64':uidb64,'token':token_generator.make_token(user)})
        
        activate_link = 'http://'+domain+link
        email_subject = 'Activate your account'
        email_body = 'Hi '+user.username+',\nPlease use this link to verify your account\n'+activate_link
        email = EmailMessage(
            email_subject,
            email_body,
            'onlyforziks@gmail.com',
            [user.email],
        )
        EmailThread(email).start()
        
        login(self.request, user)
        messages.success(self.request,'Success! Your account has been created successfully.')
        return result

class VerificationView(View):
    def get(self,request,uidb64,token):
        try:
            user_id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            if not token_generator.check_token(user,token):
                return redirect('student_course_list'+'?message='+'User already activated')

            if user.profile.is_email_confirmed:
                return redirect('student_course_list')
            user.profile.is_email_confirmed = True
            user.save()	
            messages.success(request,'Account activated successfully')
            return redirect('student_course_list')
        except Exception as e:
            pass

        return redirect('student_course_list')

class StudentEnrollCourseView(LoginRequiredMixin, FormView):
    course = None
    form_class = CourseEnrollForm

    def form_valid(self, form):
        self.course = form.cleaned_data['course']
        self.course.students.add(self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('student_course_detail',args=[self.course.id])  



class StudentCourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'students/course/list.html'
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(students__in=[self.request.user])        

class StudentCourseDetailView(DetailView):
    model = Course
    template_name = 'students/course/detail.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(students__in=[self.request.user])
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get course object
        course = self.get_object()
        if 'module_id' in self.kwargs:
            # get current module
            module = course.modules.get(id=self.kwargs['module_id'])
            context['content'] = module.contents.get(id=self.kwargs['content_id'])
            
        else:
            # get first module
            context['module'] = course.modules.all()[0]
            
        return context

@login_required(login_url = 'login')
def InstructorCreate(request):
    subjects = Subject.objects.all()
    

    if request.method == 'POST':
        username = request.user
        phone_number = request.POST['phone_number']
        dob = request.POST['dob']
        address = request.POST['address']
        bio = request.POST['bio']

        if not bool(re.search('^[9][0-9]{9}$',phone_number)):
            messages.error(request,'Please Enter a Valid Phone Number')
            return redirect('became_an_instructor')

        if Instructor.objects.filter(phone_number=phone_number).exists():
            messages.error(request,'Phone Number Already Exist')
            return redirect('became_an_instructor')
        
            

        user = User.objects.get(username=username)

        instructor = Instructor(username=username,phone_number=phone_number,dob=dob,address=address,bio=bio);
        instructor.save()
        
        group = Group.objects.get(name = 'Instructors')
        user.groups.add(group)
        user.save()
        messages.success(request,'Your Instructor account has been successfully created.')
        return redirect('manage_course_list')
    return render(request,'instructors/signup.html',{'subjects':subjects})

class ProfileView(LoginRequiredMixin,View):
    def get(self,request):
        s_form = StudentUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        i_form = None
        if User.objects.filter(username=request.user.username,groups__name="Instructors").exists():
            i_form = InstructorUpdateForm(instance=request.user.instructor)
        context = {
            's_form':s_form,
            'p_form':p_form,
            'i_form':i_form
        }
        return render(request,'students/student/profile.html',context)
    def post(self,request):
        s_form = StudentUpdateForm(request.POST,instance=request.user)
        p_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
        i_form = None;
        if User.objects.filter(username=request.user.username,groups__name="Instructors").exists():
            i_form = InstructorUpdateForm(request.POST,instance=request.user.instructor)
        
            if s_form.is_valid() and p_form.is_valid() and i_form.is_valid():
                s_form.save()
                p_form.save()
                i_form.save()
                messages.success(request,'Info has been updated')
           
            else:
                messages.error(request,s_form.errors)
        else:
            if s_form.is_valid() and p_form.is_valid():
                s_form.save()
                p_form.save()
            else:
                messages.error(request,s_form.errors)
            

        context = {
            's_form':s_form,
            'p_form':p_form,
            'i_form':i_form
        }
        
        return render(request,'students/student/profile.html',context)
            


class ChangePasswordView(LoginRequiredMixin,View):
    def get(self,request):
        form = PasswordChangeForm(request.user)
        return render(request,'accounts/change_password.html',{'form':form})
    def post(self,request):
        form = PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
            messages.success(request,'Password has been changed Successfully')
           
        else:
            messages.error(request,form.errors)
            return redirect('change_password')
        
        return render(request,'students/student/changepassword.html',{'form':form})

class CertificateView(LoginRequiredMixin,View):
    def get(self,request):
        return render(request,'students/student/certificate.html')


class EnrolledCoursesView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'students/student/enrolled_courses.html'
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(students__in=[self.request.user])  

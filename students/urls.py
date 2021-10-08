from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt
# from django.views.decorators.cache import cache_page
# from django.contrib.auth import views as auth_view


urlpatterns = [
    path('register/',views.StudentRegistrationView.as_view(),name='student_registration'),
    path('enroll-course/',views.StudentEnrollCourseView.as_view(),name='student_enroll_course'),
    path('courses/',views.StudentCourseListView.as_view(),name='student_course_list'),
    path('course/<pk>/',views.StudentCourseDetailView.as_view(),name='student_course_detail'),
    path('course/<pk>/<module_id>/<content_id>',views.StudentCourseDetailView.as_view(),name='student_course_detail_module'),
    path('became_an_instructor/',views.InstructorCreate,name="became_an_instructor"),
    path('profile/',views.ProfileView.as_view(),name='profile'),
    path('changepassword/',views.ChangePasswordView.as_view(),name='change_password'),
    path('enrolled-courses/',views.EnrolledCoursesView.as_view(),name='enrolled_courses'),
    path('certificate/',views.CertificateView.as_view(),name='certificate'),
    path('activate/<uidb64>/<token>/',views.VerificationView.as_view(),name='activate'),
    path('course-status/',csrf_exempt(views.course_status),name="course_status"),
    path('request-for-certificate/<course_id>/',views.request_for_certificate,name="request_for_certificate"),
    path('admin/report/<str:username>/', views.admin_generate_report,name='admin_generate_report'),
    path('admin/report/<str:username>/', views.admin_generate_report,name='admin_generate_report'),
    path('verify-certificate/',views.verify_certificate,name="verify_certificate"),

    
]
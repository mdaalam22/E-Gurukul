from django.contrib import admin
from .models import Subject, Course, Module,Contact,CourseContentStatus,CourseStatus,Certificate
from django.utils.html import format_html

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}
class ModuleInline(admin.StackedInline):
    model = Module


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'created']
    list_filter = ['created', 'subject']
    search_fields = ['title', 'overview']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ModuleInline]

@admin.register(CourseContentStatus)
class CourseContentStatAdmin(admin.ModelAdmin):
    list_display = ['student_username', 'course', 'module','content','completed']
    list_filter = ['student_username']
    search_fields = ['student_username', 'module','content']

@admin.register(CourseStatus)
class CourseStatusAdmin(admin.ModelAdmin):
    list_display = ['username', 'course', 'percentage','completed','date_joined']
    list_filter = ['username','course']
    search_fields = ['username', 'course']

@admin.register(Certificate)
class CertifacateAdmin(admin.ModelAdmin):
    list_display = ['username', 'course', 'certificate','code','view','date']
    list_filter = ['username','course','code']
    search_fields = ['username', 'course','code']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name','show_email','phone_number','subject','message','date')
    search_fields = ('name','email','phone_number','subject')
    list_filter = ('date',)

    def show_email(self, obj):
        return format_html("<a href='mailto:{mail}'>{mail}</a>", mail=obj.email)

admin.site.index_template = 'memcache_status/admin_index.html'    
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from .fields import OrderField
from django.template.loader import render_to_string
# from PIL import Image,ImageFont,ImageDraw
from django.conf import settings
import PIL.Image,PIL.ImageFont,PIL.ImageDraw
from datetime import date


# Create your models here.
class Subject(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='subjectImage')
    slug = models.SlugField(max_length=200,unique=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title
    
class Course(models.Model):
    owner = models.ForeignKey(User,related_name='courses_created',on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,related_name='courses',on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    thumbnail = models.ImageField(upload_to='thumbnail')
    slug = models.SlugField(max_length=200,unique=True)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    students = models.ManyToManyField(User,related_name='courses_joined',blank=True)


    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title
        
    
class Module(models.Model):
    course = models.ForeignKey(Course,related_name='modules',on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = OrderField(blank=True, for_fields=['course'])

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.order}. {self.title}'

class Content(models.Model):
    module = models.ForeignKey(Module,related_name='contents',on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType,on_delete=models.CASCADE,limit_choices_to={'model__in':('text','video','image','file')})
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    order = OrderField(blank=True, for_fields=['module']) 

    class Meta:
        ordering = ['order']   


class ItemBase(models.Model):
    owner = models.ForeignKey(User,related_name='%(class)s_related',on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True
    def __str__(self):
        return self.title
    def render(self):
        return render_to_string(
        f'courses/content/{self._meta.model_name}.html',{'item': self})  

class Text(ItemBase):
    content = models.TextField()

class File(ItemBase):
    file = models.FileField(upload_to='files')

class Image(ItemBase):
    file = models.FileField(upload_to='images')
    
class Video(ItemBase):
    url = models.URLField()        



class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=15)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
        



class CourseContentStatus(models.Model):
    student_username = models.ForeignKey(User,on_delete=models.CASCADE)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    module = models.ForeignKey(Module,on_delete=models.CASCADE)
    content = models.ForeignKey(Content,on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    class Meta:
        db_table = 'course_content_status'
        verbose_name_plural = 'course_content_status'


class CourseStatus(models.Model):
    username = models.ForeignKey(User,on_delete=models.CASCADE)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    percentage = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'course_status'
        verbose_name_plural = 'course_status'


# ========generate code for certificate======
import secrets
def random_code():
    sys_random = secrets.SystemRandom()
    secure_code = sys_random.randrange(100000, 999999)
    return secure_code


class Certificate(models.Model):
    username = models.ForeignKey(User,on_delete=models.CASCADE)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    certificate = models.ImageField(default='certificates.jpg',upload_to='certificates')
    code = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    view = models.BooleanField(default=False)

    # def save(self):
    #     super().save()

    #     name = self.username.get_full_name()
    #     course_title = self.course.title
    #     today = date.today()
    #     today_date = today.strftime("%B %d, %Y")
    #     instructor = self.course.owner.get_full_name()
    #     text1 = f"successfully completed {course_title}"
    #     text2 = f"online course on {today_date}."
    #     font1 = PIL.ImageFont.truetype('arial.ttf',100)
    #     font2 = PIL.ImageFont.truetype('arial.ttf',60)
    #     image = PIL.Image.open(self.certificate.path)
    #     draw = PIL.ImageDraw.Draw(image)
    #     draw.text(xy=(217,453),text=name,fill=(0,0,0),font=font1)
    #     draw.text(xy=(217,641),text=text1,fill=(0,0,0),font=font2)
    #     draw.text(xy=(217,710),text=text2,fill=(0,0,0),font=font2)
    #     draw.text(xy=(193,1193),text=instructor,fill=(0,0,0),font=font2)
    #     save_to_path = settings.MEDIA_ROOT+"certificates"
    #     filename = f'{self.username.username}_{course_title}'
    #     image.save(save_to_path+filename+'.jpeg')
    #     self.certificate = filename+'.jpeg'



from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def course_chat_room(request,course_id):
    try:
        course  = request.user.courses_joined.get(id=course_id)
        courses_list = request.user.courses_joined.all()
    except:
        return HttpResponseForbidden()
    
    return render(request,'chat/room.html',{'course':course,'courses_list':courses_list,
        'username':request.user.username})

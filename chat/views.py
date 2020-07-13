from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def course_chat_room(request,course_id):
    # 只有注册在这门课程里的学生才能进入这门课的聊天室
    try :
        course = request.user.courses_joined.get(id=course_id)
    except :
        return HttpResponseForbidden()
    return render(request,'chat/room.html',{'course':course})

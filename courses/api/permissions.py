from rest_framework.permissions import BasePermission

class IsEnrolled(BasePermission):
    '''检查学生是否注册到这个课程上了'''
    def has_object_permission(self,request,view,obj):
        return obj.students.filter(id=request.user.id).exists()
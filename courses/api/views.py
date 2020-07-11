from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.decorators import action

from ..models import Subject,Course
from .serializers import SubjectSerializer, CourseSerializer,\
    CourseWithContentsSerializer
from .permissions import IsEnrolled

class SubjectListView(generics.ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class SubjectDetailView(generics.RetrieveAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

""" class CourseEnrollView(APIView):
    # 验证用户身份
    authentication_classes = (BasicAuthentication,)
    # 只有验证了身份的用户才能访问
    permission_classes = (IsAuthenticated,)
    def post(self,request,pk,format=None):
        course = get_object_or_404(Course,pk=pk)
        course.students.add(request.user)
        return Response({'enrolled':True}) """


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    '''有了这个就不用一个一个地建了'''
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    
    # 装饰器说明这是在单个课程上的活动
    # 只允许post方法
    # 还说明了验证和权限使用哪个类
    @action(detail=True,
            methods=['post'],
            authentication_classes=[BasicAuthentication],
            permission_classes=[IsAuthenticated])
    def enroll(self,request,*args,**kwargs):
        course = self.get_object()
        course.students.add(request.user)
        return Response({'enrolled':True})
    
    # 会把某个课程的内容也显示出来
    @action(detail=True,
            methods=['get'],
            serializer_class=CourseWithContentsSerializer,
            authentication_classes=[BasicAuthentication],
            permission_classes=[IsAuthenticated,IsEnrolled])
    def contents(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)

    
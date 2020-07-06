from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, FormView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import CourseEnrollForm
from courses.models import Course

# Create your views here.
class StudentRegistrationView(CreateView):
    '''学生注册一个账户'''
    template_name = 'students/student/registration.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('student_course_list')

    def form_valid(self, form):
        # 返回的是HTTP response
        result = super().form_valid(form)
        cd = form.cleaned_data
        user = authenticate(username=cd['username'],
                            password=cd['password'])
        login(self.request,user)
        return result


class StudentEnrollCourseView(LoginRequiredMixin,
                              FormView):
    course = None
    form_class = CourseEnrollForm

    def form_valid(self,form):
        self.course = form.cleaned_data['course']
        self.course.students.add(self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('student_course_detail',
                            args=[self.course.id])

class StudentCourseListView(LoginRequiredMixin,
                            ListView):
    model = Course
    template_name = 'students/course/list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        # 只显示当前学生注册了的课程
        return qs.filter(students__in=[self.request.user])

class StudentCourseDetailView(DetailView):
    model = Course
    template_name = 'students/course/detail.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(students__in=[self.request.user])

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        # 获取课程对象
        course = self.get_object()
        # module_id是URL里面的参数
        if 'module_id' in self.kwargs:
            # 获取指定的模块
            context['module'] = course.modules.get(id=self.kwargs['module_id'])
        else:
            # 获取第一个模块
            context['module'] = course.modules.all()[0]
        return context




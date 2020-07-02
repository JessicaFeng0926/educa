from django import forms
from django.forms.models import inlineformset_factory

from .models import Course, Module

# 把相关的对象关联起来了
ModuleFormSet = inlineformset_factory(Course,
                                      Module,
                                      fields=['title',
                                              'description'],
                                      # 规定了一次可以编辑两个模块
                                      extra=2,
                                      # django会提供复选框
                                      # 允许勾选删除不要的表单
                                      can_delete=True)
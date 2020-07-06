from django import forms

from courses.models import Course

class CourseEnrollForm(forms.Form):
    # 这是一个用户看不到的字段
    course = forms.ModelChoiceField(queryset=Course.objects.all(),
                                    widget=forms.HiddenInput)
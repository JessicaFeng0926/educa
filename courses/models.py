from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from .fields import OrderField
# Create your models here.

class Subject(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,
                            unique=True)
    
    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

class Course(models.Model):
    # 创建这门课程的导数
    owner = models.ForeignKey(User,
                              related_name='courses_created',
                              on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,
                                related_name='courses',
                                on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,
                            unique=True)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title

class Module(models.Model):
    course = models.ForeignKey(Course,
                               related_name='modules',
                               on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    # 这是模块的序号，是我们自定义的一种字段类型
    order = OrderField(blank=True,for_fields=['course'])

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.order}. {self.title}'

class Content(models.Model):
    '''每个模块里的学习内容文件类型不确定，所以需要一个通用类'''
    module = models.ForeignKey(Module,
                               related_name='contents',
                               on_delete=models.CASCADE)
    # 这里规定了文件只能是四种类型中的一种
    content_type = models.ForeignKey(ContentType,
                                     on_delete=models.CASCADE,
                                     limit_choices_to={'model__in':(
                                         'text',
                                         'video',
                                         'image',
                                         'file'
                                     )})
    # 保存主键
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type','object_id')
    # 序号
    order = OrderField(blank=True,for_fields=['module'])

    class Meta:
        ordering = ['order']

class ItemBase(models.Model):
    '''这是各种材料的抽象基类'''
    # 这里的名字是个性化的，用class做占位符，到时候会替换成具体的类名
    owner = models.ForeignKey(User,
                              related_name='%(class)s_related',
                              on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

# 下面是具体的学习材料的类
# 它们都继承自同一个抽象基类
class Text(ItemBase):
    content = models.TextField()

class File(ItemBase):
    file = models.FileField(upload_to='files')

class Image(ItemBase):
    file = models.FileField(upload_to='images')

class Video(ItemBase):
    url = models.URLField()





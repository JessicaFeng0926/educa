from rest_framework import serializers

from ..models import Subject, Course, Module, Content


class SubjectSerializer(serializers.ModelSerializer):
    '''这是对Subject模型的序列化'''
    class Meta:
        model = Subject
        fields = ['id','title','slug']

class ModuleSerializer(serializers.ModelSerializer):
    '''Module模型的序列化'''
    class Meta:
        model = Module
        fields = ['order','title','description']

class CourseSerializer(serializers.ModelSerializer):
    '''这是对Course模型的序列化'''
    
    # 这样就能完成嵌套
    modules = ModuleSerializer(many=True,read_only=True)

    class Meta:
        model = Course
        fields = ['id','subject','title','slug','overview',
                  'created','owner','modules']

class ItemRelatedField(serializers.RelatedField):
    '''因为Content模型里的item是托管的通用类型，所以要特别声明'''
    def to_representation(self,value):
        return value.render()

class ContentSerializer(serializers.ModelSerializer):
    item = ItemRelatedField(read_only=True)

    class Meta:
        model = Content
        fields = ['order','item']


class ModuleWithContentsSerializer(serializers.ModelSerializer):
    contents = ContentSerializer(many=True)

    class Meta:
        model = Module
        fields = ['order','title','description','contents']

class CourseWithContentsSerializer(serializers.ModelSerializer):
    modules = ModuleWithContentsSerializer(many=True)

    class Meta:
        model = Course
        fields = ['id','subject','title','slug',
                  'overview','created','owner','modules']





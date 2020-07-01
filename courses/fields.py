from django.db import models
from django.core.exceptions import ObjectDoesNotExist

class OrderField(models.PositiveIntegerField):
    # 这里的for_fields参数其实相当于上一级标题
    # 举个例子，course1有2个module,那么这两个module的序号可能是0和1
    # course2目前有一个module，序号是0
    # 现在要给course2添加一个module，它的序号应该是多少呢？
    # 这是我们就把for_fields设置为['course']
    # 找到所有的module之后就要筛选出course和新module一致的作为参照
    # 所以找出来的就是course2里的那个序号为0的module
    def __init__(self, for_fields=None,*args, **kwargs):
        self.for_fields = for_fields
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        # 这里的attname是django提供的代表在当前模型里的这个字段的名字
        if getattr(model_instance,self.attname) is None:
            try:
                qs = self.model.objects.all()
                if self.for_fields:
                    query = {field:getattr(model_instance,field) \
                        for field in self.for_fields}
                    qs = qs.filter(**query)
                last_item = qs.latest(self.attname)
                value = last_item.order + 1
            except ObjectDoesNotExist:
                value = 0
            setattr(model_instance,self.attname,value)
            return value
        else:
            return super().pre_save(model_instance,add)
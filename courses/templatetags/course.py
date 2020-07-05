from django import template

register = template.Library()

@register.filter
def model_name(obj):
    try:
        # 类名是从元类里取出来的
        return obj._meta.model_name
    except AttributeError:
        return None
from django import template

register = template.Library()


@register.filter(name='filter_get')
def filter_get(value, arg):
    print(value)
    return value[str(arg)]

from django import template

register = template.Library()

@register.filter
def range(start_value, value):
    return range(start_value, value)
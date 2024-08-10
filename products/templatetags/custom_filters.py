from django import template

register = template.Library()

@register.filter
def range(start_value, value):
    return range(start_value, value)

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
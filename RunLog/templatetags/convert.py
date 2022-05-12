from django import template
register = template.Library()


@register.filter
def convert_to_positive(value):
    pos = value*-1
    return pos

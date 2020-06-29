from django import template
from django.template.defaultfilters import stringfilter
register = template.Library()

@register.filter(name='upper')
def upper(value):
    return value.upper()
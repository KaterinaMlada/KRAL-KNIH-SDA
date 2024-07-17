from django import template
from random import shuffle

register = template.Library()

@register.filter
def shuffle_list(value):
    if isinstance(value, list):
        shuffled = list(value)
        shuffle(shuffled)
        return shuffled
    else:
        return value

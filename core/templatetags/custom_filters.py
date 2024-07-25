from django import template
from random import shuffle

register = template.Library()

@register.filter
def shuffle_list(value):  
    if isinstance(value, list):  # Zkontroluje, zda je vstupní hodnota typu seznam
        shuffled = list(value)   # Vytvoří kopii seznamu
        shuffle(shuffled)    # Zamíchá prvky v seznamu
        return shuffled
    else:
        return value


@register.filter(name='add_class')
def add_class(field, css_class):
      return field.as_widget(attrs={'class': css_class}) # Přidá CSS třídu do HTML widgetu pro formulářové pole



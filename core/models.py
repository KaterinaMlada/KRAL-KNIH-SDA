from django.contrib.auth.models import User

from django.db import models
from django.db.models import Model, CharField, IntegerField  #doplnit postupne podle vsech modelu


class Author(models.Model):
    id = IntegerField(primary_key=True)
    first_name = CharField(max_length=15)
    last_name = CharField(max_length=25)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

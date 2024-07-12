from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


# Create your models here.

class Tag(models.Model):
    label = models.CharField(max_length=100)

    def __str__(self):
        return self.label


class TaggedItem(models.Model):
    #Jaky tag je ke kteremu itemu
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    #nepouzivat primo book, ale obecne typ ContentType, aby byla appka samostatne
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

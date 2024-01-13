from django.db import models
from model_utils.managers import InheritanceManager


class Node(models.Model):
    def __str__(self):
        return self.slug
    
    objects = InheritanceManager()

    slug = models.SlugField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Person(Node):
    def __str__(self):
        return f'{self.name_last}, {self.name_first}'

    name_last = models.CharField(max_length=200)
    name_first = models.CharField(max_length=200)


class Org(Node):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=200)
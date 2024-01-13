from django.contrib import admin

from .models import Node, Person, Org

admin.site.register(Node)
admin.site.register(Person)
admin.site.register(Org)

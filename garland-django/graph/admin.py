from django import forms
from django.contrib import admin
from django.forms.models import BaseInlineFormSet
from .models import Node, Edge, Person, Place, Thing, Event, Set


class SubjectInline(admin.TabularInline):
    model = Edge
    extra = 0
    fk_name = "subject"
    verbose_name = "Subject Relation"


class DobjectInline(admin.TabularInline):
    model = Edge
    extra = 0
    fk_name = "dobject"
    verbose_name = "Direct Object Relation"


class EdgeInline(admin.TabularInline):
    model = Edge
    extra = 0

    # dummy foreign key field to satisfy Django System Check (we're overriding it anyways)
    fk_name = "subject"

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        formset.instance = obj
        return formset

class NodeAdmin(admin.ModelAdmin):
    inlines = [EdgeInline]

class PersonAdmin(NodeAdmin):
    pass

class PlaceAdmin(NodeAdmin):
    pass

class ThingAdmin(NodeAdmin):
    pass

class EventAdmin(NodeAdmin):
    pass

class SetAdmin(NodeAdmin):
    pass

# admin.site.register(Node, NodeAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Place, PlaceAdmin)
admin.site.register(Thing, ThingAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Set, EventAdmin)
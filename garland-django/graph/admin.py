from django import forms
from django.contrib import admin
from django.forms.models import BaseInlineFormSet
from .models import Node, NodeRelation

class SubjectInline(admin.TabularInline):
    model = NodeRelation
    extra = 0
    fk_name = "node_subject"
    verbose_name = "Subject Relation"

class DobjectInline(admin.TabularInline):
    model = NodeRelation
    extra = 0
    fk_name = "node_dobject"
    verbose_name = "Direct Object Relation"


class CustomInlineFormSet(BaseInlineFormSet):
        def get_queryset(self):
          # Handle the case where the instance is new and unsaved
          if not hasattr(self, '_queryset'):
              if self.instance.pk is None:
                  # Instance is new and unsaved, so it cannot have any relations yet
                  self._queryset = self.model.objects.none()
              else:
                  # Get the standard queryset (forward relations)
                  qs = super().get_queryset()

                  # Get the reverse relations and combine them
                  reverse_qs = self.model.objects.filter(node_dobject=self.instance)
                  self._queryset = qs | reverse_qs

          return self._queryset

class NodeRelationInline(admin.TabularInline):
    model = NodeRelation
    formset = CustomInlineFormSet
    extra = 0

    # dummy foreign key field to satisfy Django System Check (we're overridding it anyways)
    fk_name = 'node_subject'

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        formset.instance = obj
        return formset
    

class NodeAdmin(admin.ModelAdmin):
    inlines = [NodeRelationInline]

# class NodeAdmin(admin.ModelAdmin):
#     inlines = [
#         SubjectInline,
#         DobjectInline,
#     ]

admin.site.register(Node, NodeAdmin)
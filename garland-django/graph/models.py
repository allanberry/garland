from django.db import models
from model_utils.managers import InheritanceManager


class Node(models.Model):
    def __str__(self):
        return self.slug

    objects = InheritanceManager()
    nodes = models.ManyToManyField(
        "self",
        through="NodeRelation",
        symmetrical=False,
        through_fields=("node_subject", "node_dobject"),
    )

    slug = models.SlugField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class NodeRelation(models.Model):
    kind_choices = {
        "parent_of": "parent of",
        "has_parent": "has parent",
    }

    def get_opposite_relationship(self):
        opposites = {
            "parent_of": "has_parent",
            "has_parent": "parent_of",
        }
        return opposites.get(self.kind, "parent_of")

    kind = models.CharField(max_length=200, choices=kind_choices)
    order = models.IntegerField(default=0)

    node_subject = models.ForeignKey(
        Node, related_name="has_node", on_delete=models.CASCADE
    )
    node_dobject = models.ForeignKey(
        Node, related_name="of_node", on_delete=models.CASCADE
    )


# class Person(Node):
#     def __str__(self):
#         return f"{self.name_last}, {self.name_first}"

#     name_last = models.CharField(max_length=200)
#     name_first = models.CharField(max_length=200)


# class Org(Node):
#     def __str__(self):
#         return self.name

#     name = models.CharField(max_length=200)

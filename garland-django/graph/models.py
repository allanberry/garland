from django.db import models, transaction
from model_utils.managers import InheritanceManager


class Node(models.Model):
    def __str__(self):
        return self.slug

    objects = InheritanceManager()
    nodes = models.ManyToManyField(
        "self",
        through="Edge",
        symmetrical=False,
        through_fields=("subject", "dobject"),
    )

    slug = models.SlugField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Edge(models.Model):
    CHOICES = {
        "child_of": "child of",
        "has_child": "has child",
        "spouse_of": "spouse of",
        "sibling_of": "sibling of",
        "friend_of": "friend of",
    }

    kind = models.CharField(
        max_length=200,
        choices=CHOICES,
    )

    def kind_opposite(self, key):
        return {
            "child_of": "has_child",
            "has_child": "child_of",
            "spouse_of": "spouse_of",
            "sibling_of": "sibling_of",
            "friend_of": "friend_of",
        }.get(key)

    order = models.IntegerField(default=0)

    subject = models.ForeignKey(Node, related_name="dobjects", on_delete=models.CASCADE)
    reciprocal_edge = models.OneToOneField("self", on_delete=models.CASCADE, null=True)
    dobject = models.ForeignKey(Node, related_name="subjects", on_delete=models.CASCADE)

    def save(self, checkReciprocal=True, *args, **kwargs):
        super().save(*args, **kwargs)  # Call the "real" save() method.
        if not self.reciprocal_edge:
            self.reciprocal_edge = Edge.objects.create(
                subject=self.dobject,
                kind=self.kind_opposite(self.kind),
                dobject=self.subject,
                reciprocal_edge=self,
            )
        if self.reciprocal_edge and checkReciprocal:
            self.reciprocal_edge.subject = self.dobject
            self.reciprocal_edge.kind = self.kind_opposite(self.kind)
            self.reciprocal_edge.dobject = self.subject
            self.reciprocal_edge.reciprocal_edge = self
            self.reciprocal_edge.save(checkReciprocal=False)


# class Person(Node):
#     def __str__(self):
#         return f"{self.name_last}, {self.name_first}"

#     name_last = models.CharField(max_length=200)
#     name_first = models.CharField(max_length=200)


# class Org(Node):
#     def __str__(self):
#         return self.name

#     name = models.CharField(max_length=200)

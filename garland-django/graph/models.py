from django.db import models
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
        }.get(key)

    order = models.IntegerField(default=0)

    subject = models.ForeignKey(Node, related_name="dobjects", on_delete=models.CASCADE)
    dobject = models.ForeignKey(Node, related_name="subjects", on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        creating = self._state.adding
        super(Edge, self).save(*args, **kwargs)
        if creating:
            # Check if the reciprocal edge already exists
            reciprocal_edge_exists = Edge.objects.filter(
                subject=self.dobject,
                kind=self.kind_opposite(self.kind),
                dobject=self.subject,
            ).exists()

            if not reciprocal_edge_exists:
                # Create reciprocal edge
                Edge.objects.create(
                    subject=self.dobject,
                    kind=self.kind_opposite(self.kind),
                    dobject=self.subject,
                )

    def delete(self, *args, **kwargs):
        # Find and delete the reciprocal edge
        reciprocal_edge = Edge.objects.filter(
            subject=self.dobject,
            kind=self.kind_opposite(self.kind),
            dobject=self.subject,
        ).first()
        super(Edge, self).delete(*args, **kwargs)
        if reciprocal_edge:
            reciprocal_edge.delete()

    # not yet working
    # def update(self, *args, **kwargs):
    #     # Find and update the reciprocal edge
    #     reciprocal_edge = Edge.objects.filter(
    #         subject=self.dobject,
    #         kind=self.kind_opposite(self.kind),
    #         dobject=self.subject,
    #     ).first()
    #     super(Edge, self).update(*args, **kwargs)
    #     if reciprocal_edge:
    #         reciprocal_edge.update(
    #             subject=self.dobject,
    #             kind=self.kind_opposite(self.kind),
    #             dobject=self.subject,
    #         )


# class Person(Node):
#     def __str__(self):
#         return f"{self.name_last}, {self.name_first}"

#     name_last = models.CharField(max_length=200)
#     name_first = models.CharField(max_length=200)


# class Org(Node):
#     def __str__(self):
#         return self.name

#     name = models.CharField(max_length=200)

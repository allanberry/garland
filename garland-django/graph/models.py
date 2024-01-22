from django.db import models, transaction
from django.utils.text import slugify
from model_utils.managers import InheritanceManager
import textwrap


# ------------#
# Graph Base #
# ------------#


class Node(models.Model):
    def __str__(self):
        return self.name

    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=200)
    objects = InheritanceManager()
    nodes = models.ManyToManyField(
        "self",
        through="Edge",
        symmetrical=False,
        through_fields=("subject", "dobject"),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    about = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = textwrap.shorten(slugify(self.name), width=50)
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()

        # TODO: need here to auto change slug if integrity error


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


# ----------------#
# Graph Specific #
# ----------------#


class Person(Node):
    def __str__(self):
        if self.surname:
            return f"{self.surname}, {self.name}"
        else:
            return self.name

    surname = models.CharField(max_length=200, blank=True)
    gender = models.CharField(
        max_length=20,
        blank=True,
        choices=[
            (None, "not specified"),
            ("female", "female"),
            ("male", "male"),
            ("nonbinary", "non-binary"),
        ],
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            if self.surname:
                str = f"{self.surname}, {self.name}"
            else:
                str = self.name
            self.slug = slugify(textwrap.shorten(str, width=50))
        super().save(*args, **kwargs)


class Place(Node):
    def __str__(self):
        return self.name

    kind = models.CharField(
        max_length=20,
        blank=True,
        choices=[
            (None, "not specified"),
            ("dwelling", "dwelling"),
            ("business", "business"),
        ],
    )


class Thing(Node):
    def __str__(self):
        return self.name

    is_work = models.BooleanField(null=False, default=False)
    kind = models.CharField(
        max_length=20,
        blank=True,
        choices=[
            (None, "not specified"),
            ("object", "object"),
            ("article", "article"),
            ("artwork", "artwork"),
            ("book", "book"),
            ("sculpture", "sculpture"),
            ("website", "website"),
        ],
    )


class Event(Node):
    def __str__(self):
        return self.name

    kind = models.CharField(
        max_length=20,
        blank=True,
        choices=[
            (None, "not specified"),
            ("performance", "performance"),
            ("gathering", "gathering"),
        ],
    )


class Set(Node):
    def __str__(self):
        return self.name

    kind = models.CharField(
        max_length=20,
        blank=True,
        choices=[
            (None, "not specified"),
            ("org", "organization"),
            ("collection", "object collection"),
            ("series", "event series"),
            ("bibliography", "list of works"),
        ],
    )


# ---------------#
# Graph Support #
# ---------------#

# class Time(models.Model):
#     pass

# class Location(models.Model):
#     pass

# class Web(models.Model):
#     pass

# class Email(models.Model):
#     pass

# class Phone(models.Model):
#     pass

# class Medium(models.Model):
#     pass

# class Genre(models.Model):
#     pass

# class Size(models.Model):
#     pass

from django.test import TestCase
from ..models import Person, Place, Thing, Event, Set
from django.db import transaction
from django.db.utils import IntegrityError


class GraphTestCase(TestCase):
    def setUp(self):

        # People

        self.pablo = Person.objects.create(
            name="Pablo Diego José Francisco de Paula Juan Nepomuceno María de los Remedios Cipriano de la Santísima Trinidad Martyr Patricio Clito Ruíz y",
            surname="Picasso",
            gender="male",
        )

        # self.maya = Person.objects.create(
        #     slug="picasso-maya",
        #     name="Maya",
        #     surname="Picasso",
        #     gender="female",
        # )

        # self.paulo = Person.objects.create(
        #     slug="picasso-paulo",
        #     name="Paulo",
        #     surname="Picasso",
        #     gender="male",
        # )

        # self.braque = Person.objects.create(
        #     slug="braque",
        #     name="Georges",
        #     surname="Braque",
        #     gender="male",
        # )

        # self.khokhlova = Person.objects.create(
        #     slug="khokhlova",
        #     name="Olga",
        #     surname="Khokhlova",
        #     gender="female",
        # )

        # self.walter = Person.objects.create(
        #     slug="walter",
        #     name="Marie-Thérèse",
        #     surname="Walter",
        #     gender="female",
        # )

        # self.diaghilev = Person.objects.create(
        #     slug="diaghilev",
        #     name="Serge",
        #     surname="Diaghilev",
        #     gender="male",
        # )

        # self.stein = Person.objects.create(
        #     slug="stein",
        #     name="Gertrude",
        #     surname="Stein",
        #     gender="female",
        # )

        # self.stravinsky = Person.objects.create(
        #     slug="stravinsky",
        #     name="Igor",
        #     surname="Stravinsky",
        #     gender="male",
        # )

        # self.kahnweiler = Person.objects.create(
        #     slug="kahnweiler",
        #     name="Daniel-Henri",
        #     surname="Kahnweiler",
        #     gender="male",
        # )

        # self.rosenberg = Person.objects.create(
        #     slug="rosenberg",
        #     name="Paul",
        #     surname="Rosenberg",
        #     gender="male",
        # )

        # # Places
        # self.paris = Person.objects.create(
        #     name="Paris",
        # )


        # # Things

        # # Events

        # self.armory_show = Event.objects.create(
        #     name = "Armory Show"
        # )

    def test_ok(self):
        self.assertEqual(1 + 1, 2)

        # guernica
        # Nous autres musiciens
        # La Vie

        # Lapin Agile
        # russia
        # cubism
        # analytic cubism
        # synthetic cubism
        # blue period
        # rose period
        # rosenberg
        # montmartre
        # montparnasse
        # Madrid
        # france
        # spain
        # germany
        # world war I
        # paris
        # chicago
        # Chicago Picasso

    def test_slug(self):
        self.assertTrue(self.pablo.slug)


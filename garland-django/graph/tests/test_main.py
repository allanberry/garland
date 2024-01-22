from django.test import TestCase, TransactionTestCase
from ..models import Node, Edge, Person, Place, Thing, Event, Set
from django.db import transaction
from django.db.utils import IntegrityError

# Create your tests here.


class GraphTestCase(TestCase):
    def setUp(self):
        # generic objects
        self.nodeA = Node.objects.create(slug="nodeA")
        self.nodeB = Node.objects.create(slug="nodeB")

        # people
        self.john = Person.objects.create(
            name="John", surname="Smith", gender="male"
        )
        self.jill = Person.objects.create(
            slug="jill", name="Jill", surname="Jones", gender="female"
        )
        self.jeff = Person.objects.create(
            name="Jeff",
            surname="Smith-Jones",
        )
        self.sam = Person.objects.create(
            name="Sam", surname="Smith", gender="nonbinary"
        )

        # places
        self.whitehouse = Place.objects.create(slug="whitehouse", kind="dwelling")

        # things
        self.candlestick = Thing.objects.create(
            slug="candlestick", is_work=False, kind="object"
        )
        self.demoiselles = Thing.objects.create(
            slug="demoiselles", name="Les Demoiselles d'Avignon", is_work=True, kind="artwork"
        )

        # events
        self.woodstock = Event.objects.create(slug="Woodstock Music & Art Fair", name="Woodstock", kind="performance")

        # sets
        self.oralhistory = Set.objects.create(slug="testoralhistory", name="Test Oral History", kind="collection")

    def test_ok(self):
        self.assertEqual(1 + 1, 2)

    def test_node_counts(self):
        self.assertEqual(Node.objects.all().count(), 11)
        self.assertEqual(Person.objects.all().count(), 4)
        self.assertEqual(Place.objects.all().count(), 1)
        self.assertEqual(Thing.objects.all().count(), 2)
        self.assertEqual(Event.objects.all().count(), 1)
        self.assertEqual(Set.objects.all().count(), 1)

    def test_kind_opposite(self):
        self.assertEqual(Edge.kind_opposite(self, "child_of"), "has_child")
        self.assertEqual(Edge.kind_opposite(self, "sibling_of"), "sibling_of")

    def test_edge_and_reciprocal_creation(self):
        # Create an Edge
        edge = Edge.objects.create(
            subject=self.john, kind="has_child", dobject=self.sam
        )

        # Check if the Edge is created
        self.assertTrue(
            Edge.objects.filter(subject=self.john, dobject=self.sam).exists()
        )

        # Check if the reciprocal Edge is created
        self.assertTrue(
            Edge.objects.filter(subject=self.sam, dobject=self.john).exists()
        )

        # quick double chedk that things are wired correctly
        self.assertFalse(
            Edge.objects.filter(subject=self.sam, dobject=self.jill).exists()
        )

        # check same object
        self.assertEqual(edge, edge.reciprocal_edge.edge)

    def test_edge_and_reciprocal_deletion(self):
        # Create an Edge
        edge = Edge.objects.create(
            subject=self.john, kind="has_child", dobject=self.sam
        )
        reciprocal = edge.reciprocal_edge
        edge.delete()

        # Check if the Edge and its reciprocal are deleted
        self.assertFalse(
            Edge.objects.filter(subject=self.john, dobject=self.sam).exists()
        )
        self.assertFalse(
            Edge.objects.filter(subject=self.sam, dobject=self.john).exists()
        )

    def test_multiple_edges_between_same_nodes(self):
        Edge.objects.create(subject=self.john, kind="sibling_of", dobject=self.sam)
        Edge.objects.create(
            subject=self.john, kind="has_child", dobject=self.sam
        )  # I know: gross; it's just a test

        # Check the count of edges between the same nodes
        self.assertEqual(
            Edge.objects.filter(subject=self.john, dobject=self.sam).count(), 2
        )
        self.assertEqual(
            Edge.objects.filter(subject=self.sam, dobject=self.john).count(), 2
        )
        self.assertEqual(Edge.objects.all().count(), 4)

    def test_deletion_of_node_deletes_edges(self):
        edge = Edge.objects.create(
            subject=self.john, kind="has_child", dobject=self.sam
        )
        self.assertEqual(Edge.objects.count(), 2)
        self.john.delete()

        # Check if edges associated with the deleted node are also deleted
        self.assertEqual(Edge.objects.count(), 0)

    def test_edge_creation_with_invalid_data(self):
        with self.assertRaises(IntegrityError):
            Edge.objects.create(subject=self.john, dobject=None)

    def test_update_of_node_updates_reciprocal_edge(self):
        edge = Edge.objects.create(subject=self.john, kind="child_of", dobject=self.sam)
        self.assertEqual(Edge.objects.all().count(), 2)

        edge.kind = "has_child"
        edge.save()
        self.assertEqual(Edge.objects.all().count(), 2)
        self.assertEqual(edge.reciprocal_edge.kind, "child_of")

    def test_slug_exists(self):
        self.assertTrue(self.john.slug)
        self.assertTrue(self.jill.slug)
        self.assertTrue(self.jeff.slug)
        self.assertTrue(self.sam.slug)

        # self.john = Person.objects.create(
        #     name="John", surname="Smith", gender="male"
        # )
        # self.jill = Person.objects.create(
        #     slug="jill", name="Jill", surname="Jones", gender="female"
        # )
        # self.jeff = Person.objects.create(
        #     name="Jeff",
        #     surname="Smith-Jones",
        # )
        # self.sam = Person.objects.create(
        #     name="Sam", surname="Smith", gender="nonbinary"
        # )



    def test_slug_unique_custom_(self):
        self.john_jones = Person.objects.create(
            name="John", surname="Jones"
        )
        # self.john_smith_2 = Person.objects.create(
        #     name="John", surname="Smith"
        # )

        print(self.john.slug)
        print(self.john_jones.slug)
        # print(self.john_smith_2.slug)

        # TODO: modify test to check for auto clean in Node
from django.test import TestCase, RequestFactory
from django.shortcuts import render, get_object_or_404
from cistern.forms import OrderForm
from cistern.models import Fuel, Cistern, Order, OrderStatus, \
    City, CityDistance
from datetime import datetime, timedelta
from cistern.views import CisternView, CreateOrderView, \
    IndexView, OrderListView
from django.core.urlresolvers import reverse


# --------------- MODEL TESTS ----------------------------

class FuelTest(TestCase):
    def create_Fuel(selfself, type="TestFuel"):
        return Fuel.objects.create(type=type)

    def test_Fuel_creation(self):
        fuel = self.create_Fuel()
        self.assertTrue(isinstance(fuel, Fuel))
        self.assertEqual(fuel.__str__(), fuel.type)

class CisternTest(TestCase):
    def setUp(self):
        fuel = Fuel.objects.create(type="TestFuel")
        city = City.objects.create(name="TestCity")
        self.factory = RequestFactory()
        # dunno why

    def create_cistern(self,
                       name="TestCistern",
                       max_capacity=100):
        return Cistern.objects.create(
            name=name,
            max_capacity=max_capacity,
            fuel_type=Fuel.objects.get(type="TestFuel"),
            last_location=City.objects.get(name="TestCity")
        )

    def test_Cistern_creation(self):
        cistern = self.create_cistern()
        self.assertTrue(isinstance(cistern, Cistern))
        self.assertEqual(cistern.__str__(), cistern.name)


# TODO all models like this
# class CityTest
# class CityDistanceTest
# class OrderStatusTest
# class OrderTest

# --------------- VIEWS TESTS ----------------------------

class ViewsTestCase(TestCase):
    """
    Test for views when database is not empty
    """
    def setUp(self):
        self.factory = RequestFactory()
        fuel = Fuel.objects.create(type="TestFuel")
        city = City.objects.create(name="TestCity")
        cistern = Cistern.objects.create(
            name="TestCistern",
            max_capacity=100,
            fuel_type=fuel,
            last_location=city)

    def test_index_view(self):
        request = self.factory.get(reverse('index'))
        view = IndexView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)

    # TODO all views
    # def test_cistern_view
    # def test_order_list_view
    # def test_create_order_view

# class OrderFormTest(TestCase):
# TODO not ready
#     """
#     Test if forms are correct
#     """
#     def setUp(self):
#         Order.objects.create()
#
#     def test_order_valid_form(self):
#         order = Order.objects.get()


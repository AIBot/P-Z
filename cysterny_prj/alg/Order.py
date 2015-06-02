#!/usr/bin/python
# -*- coding: latin-1 -*-
class Order(object):

    def __init__(self, fuel_amount, fuel_type, order_id, destination):
        self.fuel_amount = fuel_amount
        self.fuel_type = fuel_type
        self.order_id = order_id
        self.destination = destination
        self.realisation_time = 99999  # do wywalenia ?
        self.served = False

    def is_served(self):
        return self.served

    def get_fuel_amount(self):
        return self.fuel_amount

    def get_fuel_type(self):
        return self.fuel_type

    def get_order_id(self):
        return self.order_id

    def get_destination(self):
        return self.destination

    def set_realisation_time(self, t):
        self.realisation_time = t

    def return_as_list(self):
        return [self.order_id, self.fuel_type, self.fuel_amount, self.destination]

    def __str__(self):
        a = ' Typ: '
        b = ' Ilosc: '
        c = ' Cel: '
        return str(self.order_id) + a + str(self.fuel_type) + b + str(self.fuel_amount) + c + str(self.destination)
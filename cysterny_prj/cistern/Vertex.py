#!/usr/bin/python
# -*- coding: latin-1 -*-
import sys

class Vertex:
    def __init__(self, node):
        self.id = node

        # Slownik na sasiadow
        self.adjacent = {}

        # Odleglosc na nieskonczonosc - sys.maxint
        self.distance = sys.maxsize

        # Oznaczamy jako nieodwiedzone
        self.visited = False

        # Poprzedni
        self.previous = None

    def add_neighbour(self, neighbour, weight=0):
        self.adjacent[neighbour] = weight

    def get_connections(self):
        return self.adjacent.keys()

    def get_id(self):
        return self.id

    def get_weight(self, neighbour):
        return self.adjacent[neighbour]

    def set_distance(self, dist):
        self.distance = dist

    def get_distance(self):
        return self.distance

    def set_previous(self, prev):
        self.previous = prev

    def set_visited(self):
        self.visited = True

    #def __str__(self):
    def __unicode__(self):
        return str(self.id) + ' adjacent: ' + str([x.id for x in self.adjacent])

    def __lt__(self, other):
        return self.distance < other.distance
#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os, sys

from cistern.AlgOrder import AlgOrder
from cistern.Tank import Tank
from cistern.Vertex import Vertex
from cistern.Dijkstra import *
from cistern.Graph import Graph
from cistern.FileLoader import *
from cistern.Saver import *
import sys

class Algorithm:
    def dict_to_graph(self,my_dict_list):
        g = Graph()
        for itr in range(len(my_dict_list)):
            g.add_vertex(Vertex(my_dict_list[itr]['StartPT']))

        for itr in range(len(my_dict_list)):

            key_list = list(my_dict_list[itr])
            for itr2 in range(len(key_list)):
                # if key_list[itr2] != 'StartPT':
                if key_list[itr2] != 'StartPT':
                    g.add_edge(my_dict_list[itr]['StartPT'], key_list[itr2], my_dict_list[itr][key_list[itr2]])
        return g


    def get_graph_from_file(self,filename):
        tmdict = file_loader_nodes(filename)
        return self.dict_to_graph(tmdict)

    def get_orders_from_file(self,filename):
        alist = []
        return file_loader_order(filename, alist)


    def get_tanks_from_file(self,filename, start_pt):
        alist = []
        return file_loader_tank(filename, alist, start_pt)


    def print_all_info(self,g, orders_list, tank_list):
        print ('graf:')
        for v in g:
            for w in v.get_connections():
                vid = v.get_id()
                wid = w.get_id()
                print( '( %s , %s, %3d)'  % ( vid, wid, v.get_weight(w)))
        print(" ")
        print("zamowienia [ id - typ paliwa - rozmiar zamowienia ] : ")
        for i in range(len(orders_list)):
            print (orders_list[i])
        print(" ")
        print("dostepne cysterny [ id - max pojemnosc - komory ] : ")
        for i in range(len(tank_list)):
            print (tank_list[i])


    def sort_orders_by_fuel_amount(self,orders_list):
        to_sort = []
        for itr in range(len(orders_list)):
            to_sort.append(orders_list[itr].return_as_list())

        to_sort.sort(key=lambda x: x[2])
        to_sort = to_sort[::-1]

        new_list = []
        for itr in range(len(to_sort)):
            new_list.append(Order(to_sort[itr][2], to_sort[itr][1], to_sort[itr][0], to_sort[itr][3]))

        return new_list


    def sort_tank_by_biggest(self,tank_list):
        to_sort = []
        for itr in range(len(tank_list)):
            to_sort.append(tank_list[itr].return_as_list())

        to_sort.sort(key=lambda x: x[1])
        to_sort = to_sort[::-1]
        new_list = []
        for itr in range(len(to_sort)):
            new_list.append(Tank(to_sort[itr][0], to_sort[itr][1], to_sort[itr][2], to_sort[itr][3], to_sort[itr][4]))

        return new_list


    def get_order_realisation_time(self,order, g, start_pt):
        dijkstra(g, start_pt)  # TODO: zeby dijkstry za kazdym razem nie liczyc: drugorzedne
        target = g.get_vertex(order.destination)
        # print (target)
        path = [target.get_id()]
        shortest(target, path)
        # print 'droga : %s' % (path[::-1])
        s = 0
        for i in range(len(path)-1):
            s += g.get_vertex(path[i]).get_weight(g.get_vertex(path[i+1]))
        return s, path[::-1]

    # Uwaga: zaklada sie, ze cele w cysternach s? posortowane malej?co.
    def algorithm3(self,order_list, tank_list, g):
        tank_list = self.sort_tank_by_biggest(tank_list)
        order_list = self.sort_orders_by_fuel_amount(order_list)
        next_tank = 0
        result = []
        new_cell = -1
        while len(order_list) > 0 and len(tank_list) > 0:
            the_order = order_list[0]  # najwieksze zadanie
            the_tank = tank_list[next_tank]  # 'najlepsza' cysterna

            if the_tank.free_cells_are_left():
                realisation_time, path = self.get_order_realisation_time(the_order, g, the_tank.start_pt)
                if the_tank.work_time >= realisation_time:
                    next_tank = 0

                    if not the_order.is_served():  # should be always true
                        if new_cell < 0:
                            cell = the_tank.get_biggest_free_cell()
                        else:
                            cell = new_cell
                            new_cell = -1

                        if the_tank.cells_list[cell] <= the_order.fuel_amount:

                            the_tank.usage_list[cell] = 1
                            the_order.fuel_amount -= the_tank.cells_list[cell]
                            if the_order.fuel_amount <= 0:  # male oszustwo
                                # ORDER IS SERVED
                                the_order.served = True
                                order_list.pop(0)
                            result.append([the_order.order_id, the_tank.tank_id, cell])
                        else:
                            # next CELL
                            new_cell = the_tank.get_biggest_free_cell_for_order(the_order.fuel_amount)
                            if new_cell < 0:
                                if next_tank + 1 < len(tank_list):
                                    next_tank += 1
                                else:
                                    print ("NO GOOD TANK FOR THAT ORDER")
                                    return []
                    else:
                        result.append([the_order.order_id, the_tank.tank_id, cell])
                        order_list.pop(0)
                else:
                    if next_tank + 1 < len(tank_list):
                        next_tank += 1
                    else:
                        print ("UWAGA: ZBYT ODLEGLY PUNKT [ " + str(the_order.destination) + " ]")
                        print ("ZADANIE NIE MOZE ZOSTAC ZREALIZOWANE")
                        return []
            else:
                tank_list.pop(next_tank)
        return result


    def print_results(self,result):
        if len(result) > 0:
            print (" id zamowienia \t- id cysterny \t- komorka cysterny ")
            for i in range(len(result)):
                print (str(result[i][0]) + "\t" + str(result[i][1]) + "\t" + str(result[i][2]))

    def calc(self):
        cistern = Cistern.objects.all()
        basename = "Wroclaw"
        cistern_filename = "Cistern.csv"
        graph_filename = "Graph.csv"
        order_filename = "Order.csv"

        save_cistern(cistern_filename)
        save_city(graph_filename)
        save_orders(order_filename)

        g = self.get_graph_from_file(graph_filename)
        orders_list = self.get_orders_from_file(order_filename)
        tank_list = self.get_tanks_from_file(cistern_filename, g.get_vertex(basename))
        self.print_all_info(g, orders_list, tank_list)
        print (" ")
        self.print_results(self.algorithm3(orders_list, tank_list, g))

    # g = get_graph_from_file("nodes.csv")
    # orders_list = get_orders_from_file('Zamowienie.csv')
    # tank_list = get_tanks_from_file('Cysterny.csv', g.get_vertex(basename))
    # print_all_info(g, orders_list, tank_list)
    # print (" ")
    # print_results(algorithm3(orders_list, tank_list, g))


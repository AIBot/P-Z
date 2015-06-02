#!/usr/bin/python
# -*- coding: latin-1 -*-
from Order import Order
from Tank import Tank
from Vertex import Vertex
from Dijkstra import *
from Graph import Graph
from FileLoader import *
import sys


# TODO: UWAGA - program zaklada, ze jesli z pkt A do pkt B jedzie sie 50 min to z pkt B do pkt A jedzie sie\
# TODO: \tak samo !! P.S - posprzatam ten bajzel kiedys.. chyba
# ACHTUNG :
#  Zrezygnowa?em z heapa, bo problem mi sie zaczal komplikowac i zwariowac mozna bylo..
#  Ten pseudokod co go napisa?em te? jest troch? do dupy, ale jako szkic si? nada? :D
#  Estymacja czasu wykonania zadania jest liczona w biegu (bo trzeba badac, czy dane zadanie
#  mo?e by? przydzielone, czy te? kierowca nie zd?rzy go wykona?). Oczywi?cie nie jest to
#  optymalne trasowanie, ale to jedyna znana mi metoda szacowania, czy zadanie zmie?ci si? w
#  naszych 8h.
#  Mam tylko takie rozwi?zanie, ?e po "wyczerpaniu" czasu pracy cysterny mo?na na jej zadaniach
#  odpali? jaki?przybli?ony plecakowy i zobaczy? ile czasy zaoszcz?dzimy zmieniaj?c kolejno??
#  odwiedzania poszczególnych punktów. Je?li pozosta?y czas pracy cysterny wzro?nie do jakiej?
#  dodatniej warto?ci - to przywrócimy cysterne do obiegu (o ile ma wolne komórki).. Nie wiem
#  tylko jak bardzo nam zale?y na optymalizacji tych tras...
#  Sciezek póki co nie przechowuj?, bo czekam na jak?? opini? ;)
#  Póki co to co wywala algorytm, to przydzia? zada? cysternom z wzi?ciem pod uwag? w.w estymacji
#  czasu. To teoretycznie wystarcza do zrealizowania zadania, ale wyrysowane ?cie?ki na mapie
#  mog? wygl?da? g?upio :D
#  Acha i potrzebna jest tutaj pewna walidacja danych wejsciowych, np. algorytm odrzuca zadania
#  niemo?liwe do zrealizowania w zadanym czasie.

def dict_to_graph(my_dict_list):
    g = Graph()
    for itr in range(len(my_dict_list)):
        g.add_vertex(Vertex(my_dict_list[itr]['StartPT']))

    for itr in range(len(my_dict_list)):
        #key_list = my_dict_list[itr].keys()
        #print(key_list)
        key_list = list(my_dict_list[itr])
        #print(key_list)
        for itr2 in range(len(key_list)):
            # if key_list[itr2] != 'StartPT':
            if key_list[itr2] != 'StartPT':
                g.add_edge(my_dict_list[itr]['StartPT'], key_list[itr2], my_dict_list[itr][key_list[itr2]])
    return g


def get_graph_from_file(filename):
    tmdict = file_loader_nodes(filename)
    return dict_to_graph(tmdict)


def get_orders_from_file(filename):
    alist = []
    return file_loader_order(filename, alist)


def get_tanks_from_file(filename, start_pt):
    alist = []
    return file_loader_tank(filename, alist, start_pt)


def print_all_info(g, orders_list, tank_list):
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


def sort_orders_by_fuel_amount(orders_list):
    to_sort = []
    for itr in range(len(orders_list)):
        to_sort.append(orders_list[itr].return_as_list())

    to_sort.sort(key=lambda x: x[2])
    to_sort = to_sort[::-1]

    new_list = []
    for itr in range(len(to_sort)):
        new_list.append(Order(to_sort[itr][2], to_sort[itr][1], to_sort[itr][0], to_sort[itr][3]))

    return new_list


def sort_tank_by_biggest(tank_list):
    to_sort = []
    for itr in range(len(tank_list)):
        to_sort.append(tank_list[itr].return_as_list())

    to_sort.sort(key=lambda x: x[1])
    to_sort = to_sort[::-1]
    new_list = []
    for itr in range(len(to_sort)):
        new_list.append(Tank(to_sort[itr][0], to_sort[itr][1], to_sort[itr][2], to_sort[itr][3], to_sort[itr][4]))

    return new_list


def get_order_realisation_time(order, g, start_pt):
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
def algorithm3(order_list, tank_list, g):
    tank_list = sort_tank_by_biggest(tank_list)
    order_list = sort_orders_by_fuel_amount(order_list)
    next_tank = 0
    result = []
    new_cell = -1
    while len(order_list) > 0 and len(tank_list) > 0:
        the_order = order_list[0]  # najwieksze zadanie
        the_tank = tank_list[next_tank]  # 'najlepsza' cysterna

        if the_tank.free_cells_are_left():
            realisation_time, path = get_order_realisation_time(the_order, g, the_tank.start_pt)
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


def print_results(result):
    if len(result) > 0:
        print (" id zamowienia \t- id cysterny \t- komorka cysterny ")
        for i in range(len(result)):
            print (str(result[i][0]) + "\t" + str(result[i][1]) + "\t" + str(result[i][2]))


if __name__ == '__main__':
    basename = "Node1"
    g = get_graph_from_file("nodes.csv")
    orders_list = get_orders_from_file('Zamowienie.csv')
    tank_list = get_tanks_from_file('Cysterny.csv', g.get_vertex(basename))
    print_all_info(g, orders_list, tank_list)
    print (" ")
    print_results(algorithm3(orders_list, tank_list, g))

    pass
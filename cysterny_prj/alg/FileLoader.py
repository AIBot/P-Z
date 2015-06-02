#!/usr/bin/python
# -*- coding: latin-1 -*-
import csv
from Order import Order
from Tank import Tank


# Zwraca slownik w formie:
#   "nazwawezla": dystans (int)
#   klucz "StartPT" jest zarezerwowany dla przechowania
#   nazwy wezla startowego
# Oczekiwany plik to csv zapisany wg. wzoru:
# <NazwaNodaStartowego>,<wezel I>,<dystans do I>,<wezel II>,<dyst. do II> itd..
# TODO opis dzialania i uzycia reszty w razie potrzeby skorzystania w projekcie

# [PRZYKLADOWY SPOSOB UZYCIA]
# if __name__ == '__main__':
#     # wczytywanie danych cysterny, zamowienia, punkty
#
#     orders_list = []
#     orders_list = file_loader_order('Zamowienie.csv', orders_list)
#
#     tank_list = []
#     tank_list = file_loader_tank('Cysterny.csv', tank_list)
#
#     for i in range(len(orders_list)):
#         print (orders_list[i])
#
#     for i in range(len(tank_list)):
#         print (tank_list[i])
#
#     # wyliczamy Dijkstre dla wszystkich punktow od naszej bazy
#     # algorytm realizacji zamowienia
#     pass


def file_loader_nodes(file_name):
    # fl = open(file_name, "rb")
    fl = open(file_name, "rt", encoding="UTF-8")
    data = csv.reader(fl)
    data = [row for row in data]
    fl.close()
    tmpdict = {}
    for i in range(len(data)):
        one_row = data[i]
        node = ""
        distance = 0
        for j in range(len(one_row)):
            if j == 0:
                start_point = one_row[j]
                tmpdict[i] = {"StartPT": start_point}
            else:
                if j % 2 == 1:
                    node = one_row[j]
                    tmpdict[i].update({node: 0})
                else:
                    distance = one_row[j]
                    tmpdict[i][node] = int(distance)
    return tmpdict


def file_loader_order(file_name, tmp_list):
    fl = open(file_name, "r")
    data = csv.reader(fl)
    data = [row for row in data]
    fl.close()
    for i in range(len(data)):
        one_row = data[i]
        fuel_amount = 0
        for j in range(len(one_row)):
            if j == 0:
                order_id = int(one_row[j])
            elif j == 1:
                destination = one_row[j]
            else:
                if j % 2 == 0:
                    fuel_type = int(one_row[j])
                else:
                    capacity = int(one_row[j])
                    fuel_amount += capacity
        tmp_list.append(Order(fuel_amount, fuel_type, order_id, destination))
    return tmp_list


def file_loader_tank(file_name, tmp_list, start_pt):
    fl = open(file_name, "r")
    data = csv.reader(fl)
    data = [row for row in data]
    fl.close()
    cells = []
    for i in range(len(data)):
        one_row = data[i]
        fuel_amount = 0
        cells[:] = []
        for j in range(len(one_row)):
            if j == 0:
                tank_id = int(one_row[j])
            else:
                cell_capacity = int(one_row[j])
                cells.append(cell_capacity)
                fuel_amount += cell_capacity
        tmp_list.append(Tank(cells, fuel_amount, tank_id, 320, start_pt))
    return tmp_list


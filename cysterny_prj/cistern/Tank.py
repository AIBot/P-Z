#!/usr/bin/python
# -*- coding: latin-1 -*-

# TODO: sety i gety !

class Tank(object):

    time_left = 8

    def __init__(self, cells_list, capacity, tank_id, work_time, start_pt):
        self.tank_id = tank_id
        self.capacity = capacity
        # w pliku komory sa ulozone od najwiekszej od najmniejszej
        self.cells_list = cells_list [:]
        self.work_time = work_time
        self.usage_list = [0]*len(cells_list)
        self.start_pt = start_pt
        self.tanks_path = []
        self.order_id_list = []

    def get_biggest_free_cell(self):
        for i in range(len(self.usage_list)):
            if self.usage_list[i] == 0:
                return i
        return -1

    def get_biggest_free_cell_for_order(self, amount):
        for i in range(len(self.usage_list)):
            if self.usage_list[i] == 0:
                if self.cells_list[i] <= amount:
                    return i
        return -1

    def time_decreaser(self, realisation_time, order_id):
        for i in range(len(self.order_id_list)):
            if self.order_id_list[i] == order_id:
                return
        self.order_id_list.append(order_id)
        self.work_time -= realisation_time

    def set_actuall_pt(self, pt):
        self.actuallPt = pt

    def get_capacity(self):
        return self.capacity

    def get_cells_list(self):
        return self.cells_list

    def return_as_list(self):
        return [self.get_cells_list(), self.get_capacity(), self.tank_id, self.work_time, self.start_pt]

    def free_cells_are_left(self):
        count = 0
        for i in range(len(self.usage_list)):
            if self.usage_list[i] != 0:
                count += 1
        if count == len(self.usage_list):
            return False
        else:
            return True

    def get_work_time(self):
        return self.work_time

    def __str__(self):
        a = ' Calkowita Pojemnosc: ' # dla skrocenia linii.
        b = ' Pojemnosc komor: '
        c = ' Czas pracy: '
        return str(self.tank_id) + a + str(self.capacity) + b + str(self.cells_list) + c + str(self.work_time)

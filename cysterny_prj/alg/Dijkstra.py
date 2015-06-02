#!/usr/bin/python
# -*- coding: latin-1 -*-
import heapq

# G - graf
# w - wagi
# s - wierzcholek startowy
# d - zawiera najkrotsze drogi do wszystkich wierzcholkow z wierzcholka s.
# -------------------------------------------------------------------------
# Pseudokod:
# Dijkstra(G,w,s):
#    dla kazdego wierzcholka v w V[G] wykonaj
#       d[v] := nieskonczonosc
#       poprzednik[v] := niezdefiniowane
#    d[s] := 0
#    Q := V
#    dopoki Q niepuste wykonaj
#       u := Zdejmij_Min(Q)
#       dla kazdego wierzcholka sasiada v - sasiada u wykonaj
#          jezeli d[v] > d[u] + w(u, v) to
#             d[v] := d[u] + w(u, v)
#             poprzednik[v] := u
#             Dodaj(Q, v)
#
#    Wyswietl("Droga wynosi: " + [v])
# -------------------------------------------------------------------------


# v = cel -> funkcja rekurencyjna: podaje najkrotsza sciezke (po nazwach wezlow)
def shortest(v, path):
    if v.previous:
        path.append(v.previous.get_id())
        shortest(v.previous, path)
    return


# Funkcja przyjmuje graf i wierzcholek, dla którego wyliczamy trasy
def dijkstra(a_graph, start):
    # Waga z pierwszego wezla
    start.set_distance(0)

    # dystans (waga) + wierzcholek do kolejki nieodwiedzonych
    unvisited_queue = [(v.get_distance(), v) for v in a_graph]
    heapq.heapify(unvisited_queue)

    while len(unvisited_queue):
        # Z dokumentacji: heappop: Pop and return the smallest item from the heap,
        # maintaining the heap invariant.
        # Bierzemy najbilzszy nieodwiedzony wierzcholek
        uv = heapq.heappop(unvisited_queue)
        current = uv[1]
        current.set_visited()

        # for next in v.adjacent:
        for next in current.adjacent:
            # Pomijamy zwiedzone wezly
            if next.visited:
                continue
            new_dist = current.get_distance() + current.get_weight(next)

            if new_dist < next.get_distance():
                next.set_distance(new_dist)
                next.set_previous(current)

            #     # Notka osobista: Python WTF: linie moga byc za dugie
            #     print ('updated : current = %s next = %s new_dist = %s') \
            #         % (current.get_id(), next.get_id(), next.get_distance())
            # else:
            #     print ('not updated : current = %s next = %s new_dist = %s') \
            #         % (current.get_id(), next.get_id(), next.get_distance())

        while len(unvisited_queue):
            heapq.heappop(unvisited_queue)
        unvisited_queue = [(v.get_distance(), v) for v in a_graph if not v.visited]
        heapq.heapify(unvisited_queue)



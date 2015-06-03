import csv

from cistern.models import *


def save_city(filename):
    cid = 0
    cities = City.objects.all()
    distances = CityDistance.objects.all()
    with open( filename, 'w' ) as f:
        wrt = csv.writer(f)
        for city in cities:
            row = []
            row += [str(city)]

            cid =city.id # aby sie nie powtarzaly
            for dist in distances:
                if(dist.from_city == city) and (dist.to_city.id > cid):
                    row += [str(dist.to_city)]
                    row += [str(dist.distance)]
                pass
            #ist.from_city
            if len(row) > 1:  # ay  nie bylo pustego miasta bez odleglosc
                wrt.writerow(row)
        pass


def save_cistern(filename):
    cistern_list = Cistern.objects.all()
    with open( filename, 'w' ) as f:
        wrt = csv.writer(f)
        for cistern in cistern_list:
            row = []
            row += [str(cistern.id)]
            containers = []  # for sorting
            for cont in cistern.fuelcontainer_set.all():
                if not cont.is_loaded():
                    containers += [cont.max_capacity]
            containers.sort(reverse=True)
            row += containers

            wrt.writerow(row)


def save_orders(filename):
    order_list = Order.objects.all()
    with open( filename, 'w' ) as f:
        wrt = csv.writer(f)
        for orderr in order_list:
            if orderr.status.status == 0:  # recieved
            #if True:
                row = []
                row += [str(orderr.id)]
                row += [str(orderr.to_city)]
                row += [str(orderr.fuel_type.id)]
                row += [orderr.order_capacity]
                wrt.writerow(row)



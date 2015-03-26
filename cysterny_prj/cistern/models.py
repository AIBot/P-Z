from django.db import models
from datetime import datetime


class Fuel(models.Model):
    type = models.CharField(max_length=10)

    def __str__(self):
        return self.type


class FuelContainer(models.Model):
    type = models.ForeignKey(Fuel)
    max_capacity = models.IntegerField()
    cistern = models.ForeignKey('Cistern')
    order = models.ForeignKey('Order', blank=True, null=True, default=0)

    def __str__(self):
        return "%s %s" % (self.type, self.max_capacity)

    def is_loaded(self):
        if self.order is None:
            return False
        else:
            return True



class Cistern(models.Model):
    name = models.CharField(max_length=20)
    status = models.SmallIntegerField(choices=(
        (0, 'Ready'),
        (1, 'Busy')
    ), default=0)
    remaining_time = models.IntegerField(default=8)
    last_location = models.ForeignKey('City')
    # TODO jezeli w drodze to nie w miescie
    distance_from = models.IntegerField(default=0)

    def max_capacity(self):
        mm = 0
        for container in self.fuelcontainer_set.all():
            mm = mm+container.max_capacity

        return mm

    def capacity(self):
        c = 0
        for container in self.fuelcontainer_set.all():
            if container.is_loaded():
                c = c+container.max_capacity
        return c

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name


class CityDistance(models.Model):
    from_city = models.ForeignKey(City, related_name='source_city')
    to_city = models.ForeignKey(City, related_name='destination_city')
    distance = models.IntegerField()

    def __str__(self):
        return '%s -> %s' % (self.from_city, self.to_city)


class OrderStatus(models.Model):
    #status = models.CharField(max_length=15)
    status = models.SmallIntegerField(choices=(
        (0, 'recieved'),
        (1, 'in progress'),
        (2, 'fullfilled'),
    ), default=0)

    def __str__(self):
        return "%s" % (self.get_status_display())


class Order(models.Model):
    #path = models.ForeignKey(CityDistance)
    # to_city = models.ForeignKey(City, related_name='city_order_to')
    to_city = models.ForeignKey(City)
    fuel_type = models.ForeignKey(Fuel)
    order_capacity = models.IntegerField()
    status = models.ForeignKey(OrderStatus)
    data = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return self.data.isoformat()

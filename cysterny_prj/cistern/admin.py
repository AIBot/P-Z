from django.contrib import admin
from cistern.models import Fuel, Cistern, City, \
    OrderStatus, Order, CityDistance, FuelContainer, \
    Path

class FuelAdmin(admin.ModelAdmin):
     fields = ['type']


class FuelContainerInline(admin.TabularInline):
    model = FuelContainer
    extra = 0

class CisternAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'capacity', 'max_capacity')
    inlines = [FuelContainerInline]


class CityAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name']}),
        ]


class OrderAdmin(admin.ModelAdmin):
    list_display = ('data', 'order_capacity')
    inlines = [FuelContainerInline]

class PathAdmin(admin.ModelAdmin):
    list_display = ('cistern', 'elapsed_time')

admin.site.register(Fuel, FuelAdmin)
admin.site.register(FuelContainer)
admin.site.register(Cistern, CisternAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(OrderStatus)
admin.site.register(Order, OrderAdmin)
admin.site.register(CityDistance)
admin.site.register(Path, PathAdmin)


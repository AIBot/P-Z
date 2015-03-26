from django.contrib import admin
from cistern.models import Fuel, Cistern, City, \
    OrderStatus, Order, CityDistance, FuelContainer

class FuelAdmin(admin.ModelAdmin):
     fields = ['type']


#
# class FuelInline(admin.TabularInline):
#     model = Cistern.fueltype.
#     extra = 0
#class FuelContainerAdmin(admin.ModelAdmin):
#    list_display = ('max_capacity', 'is_loaded')

#class CisternAdmin(admin.ModelAdmin):
    #list_display = ('name', 'capacity', 'status', 'max_capacity')
    # fields = ['name', 'capacity']
    # inlines = [FuelInline]
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
    #list_display = ('name')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('data', 'order_capacity')
    inlines = [FuelContainerInline]


admin.site.register(Fuel, FuelAdmin)
admin.site.register(FuelContainer)
admin.site.register(Cistern, CisternAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(OrderStatus)
admin.site.register(Order, OrderAdmin)
admin.site.register(CityDistance)


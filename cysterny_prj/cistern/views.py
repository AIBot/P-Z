from django.shortcuts import render, get_object_or_404, render_to_response
from cistern.models import Cistern, CityDistance, \
    City, Order, OrderStatus, Fuel, FuelContainer, Path
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib import messages
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.views.generic import TemplateView, FormView, CreateView, \
    UpdateView, DeleteView
from cistern.forms import OrderForm
from cistern.Algorithm import *


class IndexView(TemplateView):
    template_name = "cistern/index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        return context


class CisternView(TemplateView):
    template_name = "cistern/cistern.html"

    def get_context_data(self, **kwargs):
        context = super(CisternView, self).get_context_data(**kwargs)
        context['cistern_list'] = Cistern.objects.all()
        return context

class CisternDetailView(TemplateView):
    template_name = "cistern/cistern_detail.html"

    def get_context_data(self, **kwargs):
        cistern_id = kwargs['cistern_id']
        context = super(CisternDetailView, self).get_context_data(**kwargs)
        context['cistern'] = get_object_or_404(Cistern, pk=cistern_id)
        context['fuel_container'] = FuelContainer.objects.filter(cistern__id=cistern_id)
        return context

class OrderListView(TemplateView):
    template_name = "cistern/order_list.html"

    def get_context_data(self, **kwargs):
        context = super(OrderListView, self).get_context_data(**kwargs)
        context['order_list'] = Order.objects.all()
        return context


class CreateOrderView(CreateView):
    template_name = "cistern/order_form.html"
    success_url = reverse_lazy('index')
    model = Order
    form_class = OrderForm

    def form_valid(self, form):
        new_order = form.save(commit=False)
        new_order.status = get_object_or_404(OrderStatus, status=0)
        new_order.save()
        messages.success(self.request, 'Zamówienie przyjęte do realizacji.')
        return super(CreateOrderView, self).form_valid(form)


class PathListView(TemplateView):
    template_name="cistern/path_list.html"

    def get_context_data(self, **kwargs):
        context = super(PathListView, self).get_context_data(**kwargs)
        context['path_list'] = Path.objects.all()
        return context

class CalcView(TemplateView):
    template_name = "cistern/calc.html"

    def get_context_data(self, **kwargs):
        context = super(CalcView, self).get_context_data(**kwargs)
        alg = Algorithm()
        results = alg.calc()
        self.add_results_to_db(results=results)
        return context

    def add_results_to_db(self, results):
        last_city = get_object_or_404(City, name="Wroclaw")
        for i in range(len(results)):
            order = Order.objects.filter(id=results[i][0])
            order.update(
                status=get_object_or_404(OrderStatus, status=1)
            )
            ord2 = get_object_or_404(Order, id=results[i][0])
            cistern = Cistern.objects.filter(id=results[i][1] )
            cistern.update(status=1)
            cistern = get_object_or_404(Cistern, id=results[i][1])
            j = 0
            for fuel in cistern.fuelcontainer_set.all():  # dodac paliwa w cysternie
                j = j+1
                if j == results[i][2]:  # paliwa id do zmiany
                    print(j, ord2.fuel_type)
                    fuel.order = ord2
                    fuel.type = ord2.fuel_type
                    fuel.save()
                    break
            order = Order.objects.filter(id=results[i][0])
            city = get_object_or_404(City,
                                     name=ord2.to_city.name)
            if city != last_city:  # sciezka
                n_city2 = CityDistance.objects.get(
                        from_city=last_city,
                        to_city=city
                )
                path = Path(cistern=cistern)
                path.save()
                path.n_city.add(n_city2)

            last_city = city
        pass


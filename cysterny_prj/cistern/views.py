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
        context['order_list'] = AlgOrder.objects.all()
        return context


class CreateOrderView(CreateView):
    template_name = "cistern/order_form.html"
    success_url = reverse_lazy('index')
    model = AlgOrder
    form_class = OrderForm

    def form_valid(self, form):
        new_order = form.save(commit=False)
        new_order.status = get_object_or_404(OrderStatus, status=0)
        new_order.save()
        messages.success(self.request, 'Zamówienie przyjęte do realizacji.')
        alg = Algorithm()
        alg.calc()


        return super(CreateOrderView, self).form_valid(form)


class PathListView(TemplateView):
    template_name="cistern/path_list.html"

    def get_context_data(self, **kwargs):
        context = super(PathListView, self).get_context_data(**kwargs)
        context['path_list'] = Path.objects.all()
        return context




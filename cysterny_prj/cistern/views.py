from django.shortcuts import render, get_object_or_404, render_to_response
from cistern.models import Cistern, CityDistance, \
    City, Order, OrderStatus, Fuel, FuelContainer, Path
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib import messages
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.views.generic import TemplateView, FormView, CreateView, \
    UpdateView, DeleteView
from cistern.forms import OrderForm, CalcForm, LoginForm
from cistern.Algorithm import *
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import REDIRECT_FIELD_NAME, login, logout
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django import template

register = template.Library()

class LoginRequiredMixin(object):
    u"""Ensures that user must be authenticated in order to access view."""

    @method_decorator(login_required(redirect_field_name=reverse_lazy('index'), login_url=reverse_lazy('login')))
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)

class PermissionRequiredMixin(object):
    permission_required = ()

    @method_decorator(login_required(redirect_field_name=reverse_lazy('index'), login_url=reverse_lazy('login')))
    def dispatch(self, request, *args, **kwargs):
        if request.user.has_perm(self.permission_required):
            return super(PermissionRequiredMixin, self).dispatch(
                request, *args, **kwargs)
        else:
            return render(request, 'cistern/403.html', status=403)

class LoginView(FormView):
    """
    Provides the ability to login as a user with a username and password
    """
    template_name = "cistern/login.html"
    success_url = reverse_lazy('index')
    form_class = LoginForm
    redirect_field_name = REDIRECT_FIELD_NAME

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        # Sets a test cookie to make sure the user has cookies enabled
        request.session.set_test_cookie()

        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())

        # If the test cookie worked, go ahead and
        # delete it since its no longer needed
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()

        return super(LoginView, self).form_valid(form)

    def get_success_url(self):
        redirect_to = self.request.REQUEST.get(self.redirect_field_name)
        if not is_safe_url(url=redirect_to, host=self.request.get_host()):
            redirect_to = self.success_url
        return redirect_to

class LogoutView(TemplateView):
    template_name = "cistern/logout.html"

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


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

class OrderDetailView(TemplateView):
    template_name="cistern/order_detail.html"

    def get_context_data(self, **kwargs):
        order_id = kwargs['order_id']
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        the_order=get_object_or_404(Order, pk=order_id)
        context['order'] = the_order
        fuel_containers=FuelContainer.objects.filter(order=the_order)
        cisterns=[]
        for fc in fuel_containers:
            jest=False
            for cc in cisterns:
                if cc.id == fc.cistern.id:
                    jest=True
                    break
            if not jest:
                cisterns+=[fc.cistern]
        context['cisterns'] = cisterns
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


class PathListView(PermissionRequiredMixin, TemplateView):
    template_name="cistern/path_list.html"

    def get_context_data(self, **kwargs):
        context = super(PathListView, self).get_context_data(**kwargs)
        context['path_list'] = Path.objects.all()
        return context

class CisternCleanUpView(PermissionRequiredMixin, FormView):
    template_name = "cistern/path_delete.html"
    form_class = CalcForm
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super(CisternCleanUpView, self).get_context_data(**kwargs)
        context['msg_conf'] = "Czy usunąć zamówienia?"
        return context

    def clear_cistern(self): # cisterns orders
        cisterns = Cistern.objects.all()
        for cist in cisterns:
            cist.status = 0 # ready
            cist.save()
        stat = get_object_or_404( OrderStatus, status=1)
        Order.objects.filter(status=stat).delete()

    def form_valid(self, form):
        self.clear_cistern()
        messages.success(self.request, 'Usunięto zamówienia.')
        return super(CisternCleanUpView, self).form_valid(form)

class DeletePathView(PermissionRequiredMixin, FormView):
    template_name = "cistern/path_delete.html"
    form_class = CalcForm
    success_url = reverse_lazy('index')

    # @register.inclusion_tag(template_name, takes_context=True)
    def clear_paths(self):
        Path.objects.all().delete()

    def get_context_data(self, **kwargs):
        context = super(DeletePathView, self).get_context_data(**kwargs)
        context['msg_conf'] = "Czy usunąć ścieżki?"
        return context

    def form_valid(self, form):
        self.clear_paths()
        messages.success(self.request, 'Usunięto ścieżki.')
        return super(DeletePathView, self).form_valid(form)

class ManageView(PermissionRequiredMixin, TemplateView):
    template_name = "cistern/calc.html"


class CalcView(PermissionRequiredMixin, FormView):
    template_name = "cistern/path_delete.html"
    form_class = CalcForm
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super(CalcView, self).get_context_data(**kwargs)
        context['msg_conf'] = "Czy przeliczyć trasy?"
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
            j = -1
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


    def form_valid(self, form):
        alg = Algorithm()
        results = alg.calc()
        self.add_results_to_db(results=results)
        messages.success(self.request, 'Przeliczono trasy.')

        return super(CalcView, self).form_valid(form)


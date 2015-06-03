from django import forms
from cistern.models import Order
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, Hidden, HTML
from crispy_forms.bootstrap import FormActions, StrictButton, Field
from django.core.urlresolvers import reverse
from django.contrib.auth.forms import AuthenticationForm



class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['to_city', 'fuel_type', 'order_capacity']

    helper = FormHelper()

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-2'

        self.helper.form_id = 'id-OrderForm'
        self.helper.form_method = 'post'
        self.helper.form_action = '.'
        self.helper.layout = Layout(
            Field('to_city'),
            Field('fuel_type'),
            Field('order_capacity'),
            #Hidden('status', value=0),
            Submit("submit", "Zapisz",  css_class='btn btn-primary'),
            HTML("""<a class="btn btn-default" href="{% url 'index' %}">Anuluj</a> <br>"""),

        )

class CalcForm(forms.Form):
    helper = FormHelper()

    def __init__(self, *args, **kwargs):
        super(CalcForm, self).__init__(*args, **kwargs)
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-1'
        self.helper.field_class = 'col-lg-1'

        self.helper.form_id = 'id-CalcForm'
        self.helper.form_method = 'post'
        self.helper.form_action = '.'
        self.helper.layout = Layout(
            Submit("submit", "Przelicz",  css_class='btn btn-primary'),
            HTML("""<a class="btn btn-default" href="{% url 'index' %}">Anuluj</a> <br>"""),

        )


class LoginForm(AuthenticationForm):
    helper = FormHelper()

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-6'
        self.helper.layout = Layout(
            Field('username', placeholder="Username"),
            Field('password', placeholder="Password"),
            Submit('submit', "Zaloguj", css_class='btn btn-primary'),
)




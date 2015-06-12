from django.conf.urls import patterns, include, url
from django.contrib import admin
from cistern.views import IndexView, OrderListView, CisternView, \
    CreateOrderView, CisternDetailView, PathListView, CalcView, \
    LoginView, LogoutView, OrderDetailView, DeletePathView, \
    CisternCleanUpView, ManageView
#
# urlpatterns = patterns('',
#
#     # Examples:
#     # url(r'^$', 'cysterny_prj.views.home', name='home'),
#     # url(r'^blog/', include('blog.urls')),
#
urlpatterns = [
    url(r'^$', IndexView.as_view(), name="index"),
    url(r'^cistern/$', CisternView.as_view(), name="cistern"),
    url(r'^cistern/(?P<cistern_id>[0-9]+)$', CisternDetailView.as_view(), name="cistern_detail"),
    url(r'^orders/(?P<order_id>[0-9]+)$', OrderDetailView.as_view(), name="order_detail"),
    url(r'^orders/$', OrderListView.as_view(), name="order_list"),
    url(r'^order/$', CreateOrderView.as_view(), name="create_order"),
    url(r'^paths/$', PathListView.as_view(), name="path_list"),
    url(r'^paths_del/$', DeletePathView.as_view(), name="path_del"),
    url(r'^order_del/$', CisternCleanUpView.as_view(), name="order_del"),
    url(r'^manage/$', ManageView.as_view(), name="manage"),
    url(r'^calc/$', CalcView.as_view(), name="calc"),
    url(r'^login/$', LoginView.as_view(), name="login"),
    url(r'^logout/$', LogoutView.as_view(), name="logout"),
    url(r'^admin/', include(admin.site.urls)),
]
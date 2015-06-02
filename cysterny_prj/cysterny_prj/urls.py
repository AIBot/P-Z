from django.conf.urls import patterns, include, url
from django.contrib import admin
from cistern.views import IndexView, OrderListView, CisternView, \
    CreateOrderView, CisternDetailView, PathListView
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
    url(r'^orders/$', OrderListView.as_view(), name="order_list"),
    url(r'^order/$', CreateOrderView.as_view(), name="create_order"),
    url(r'^paths/$', PathListView.as_view(), name="path_list"),
    url(r'^admin/', include(admin.site.urls)),
]
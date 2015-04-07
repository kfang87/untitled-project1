from django.conf.urls import url
from untitledproject1.nomeste import views

urlpatterns = [
    url(r'^epnumos/$', views.nomeste_list),
    url(r'^epnumos/(?P<pk>[0-9]+)/$', views.nomeste_detail),
]
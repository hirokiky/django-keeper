from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^team/manage/$', views.team_manage),
    url(r'^team/$', views.team_dashboard),
    url(r'^account/billing/$', views.team_billing),
    url(r'^account/billing/resign/$', views.team_billing_resign),
    url(r'^$', views.dashboard),
    url(r'^magazines/(?P<magazine_id>\d+)/$', views.magazine_detail),
    url(r'^magazines/(?P<magazine_id>\d+)/(?P<article_id>\d+)/$', views.article_detail),
]

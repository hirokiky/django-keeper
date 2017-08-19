from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^team/manage/$', views.team_manage, name='team_manage'),
    url(r'^team/$', views.team_dashboard, name='team_dashboard'),
    url(r'^team/billing/$', views.team_billing, name='team_billing'),
    url(r'^team/billing/resign/$', views.team_billing_resign, name='team_billing_resign'),
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^magazines/(?P<magazine_id>\d+)/$', views.magazine_detail, name='magazine_detail'),
    url(r'^magazines/(?P<magazine_id>\d+)/(?P<article_id>\d+)/$', views.article_detail,
        name='article_detail'),
]

from django.urls import path
from . import views
from home.dash_apps.finished_apps import simpleexample

urlpatterns = [
    path('', views.home, name='dash-home'),
    path('home/', views.home, name='dash-home'),
    path('graph1/', views.graph1, name='dash-graph1'),

]
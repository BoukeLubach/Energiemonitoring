from django.urls import path
from . import views
from plant_dashboards.dash_apps import hotoil_dashapp
from plant_dashboards.dash_apps import poly_dashapp
from plant_dashboards.dash_apps import sqltags

urlpatterns = [
    path('Poly-steam/', views.poly_steam, name='poly-steam-page'),
    
    path('Recovery-steam/', views.recovery_steam, name='recovery-steam-page'),
    path('Recovery-hot-oil/', views.recovery_hot_oil, name='recovery-hot-oil-page'),
    
    path('PPD-steam/', views.ppd_steam, name='PPD-steam-page'),
    path('PPD-hot-oil/', views.ppd_hot_oil, name='PPD-hot-oil-page'),
    
    path('TDC-steam/', views.tdc_steam, name='TDC-steam-page'),
    path('TDC-hot-oil/', views.tdc_hot_oil, name='TDC-hot-oil-page'),
    

    path('utilities-steam/', views.utilities_steam, name='utilities-steam-dashboard'),
    path('utilities-hot-oil/', views.utilities_hot_oil, name='utilities-hot-oil-dashboard'),
    path('utilities-electricity/', views.utilities_electricity, name='utilities-electricity-dashboard'),
 ]
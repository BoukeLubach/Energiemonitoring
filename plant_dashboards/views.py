from django.shortcuts import render
from plotly.offline import plot
import plotly.graph_objects as go
# Create your views here.


def poly_steam(request):
    
    context = {}
    
    return render(request, 'plant_dashboards/poly_steam.html', context)



def recovery_steam(request):
    context = {}
    return render(request, 'plant_dashboards/recovery_steam.html',context)

def recovery_hot_oil(request):
    context = {}
    return render(request, 'plant_dashboards/recovery_hot_oil.html',context)



def ppd_steam(request):
    context = {}
    return render(request, 'plant_dashboards/PPD_steam.html',context )

def ppd_hot_oil(request):
    context = {}
    return render(request, 'plant_dashboards/PPD_dashboard.html',context )



def tdc_steam(request):
    context = {}
    return render(request, 'plant_dashboards/tdc_steam.html',context )

def tdc_hot_oil(request):
    context = {}
    return render(request, 'plant_dashboards/tdc_hot_oil.html',context )



def utilities_steam(request):
    context = {}
    return render(request, 'plant_dashboards/utilities_steam.html',context )

def utilities_hot_oil(request):
    context = {}
    return render(request, 'plant_dashboards/utilities_hot_oil.html',context )

def utilities_electricity(request):
    context = {}
    return render(request, 'plant_dashboards/utilities_electricity.html',context )

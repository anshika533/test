from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    path('vehicles/', views.vehicle_list, name='vehicle_list'),
    path('vehicles/add/', views.vehicle_create, name='vehicle_create'),

    path('drivers/', views.driver_list, name='driver_list'),
    path('drivers/add/', views.driver_create, name='driver_create'),

    path('trips/', views.trip_list, name='trip_list'),
    path('trips/add/', views.trip_create, name='trip_create'),
    path('trips/<int:pk>/dispatch/', views.trip_dispatch, name='trip_dispatch'),
    path('trips/<int:pk>/complete/', views.trip_complete, name='trip_complete'),
    path('trips/<int:pk>/cancel/', views.trip_cancel, name='trip_cancel'),

    path('maintenance/', views.maintenance_list, name='maintenance_list'),
    path('maintenance/add/', views.maintenance_create, name='maintenance_create'),
    path('maintenance/<int:pk>/close/', views.maintenance_close, name='maintenance_close'),

    path('fuel-logs/', views.fuel_log_list, name='fuel_log_list'),
    path('fuel-logs/add/', views.fuel_log_create, name='fuel_log_create'),

    path('reports/', views.reports, name='reports'),
]
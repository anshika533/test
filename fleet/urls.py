from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    # Vehicle
    path('vehicles/', views.vehicle_list, name='vehicle_list'),
    path('vehicles/add/', views.vehicle_create, name='vehicle_create'),

    # Driver
    path('drivers/', views.driver_list, name='driver_list'),
    path('drivers/add/', views.driver_create, name='driver_create'),

    # Trip
    path('trips/', views.trip_list, name='trip_list'),
    path('trips/add/', views.trip_create, name='trip_create'),
    path('trips/<int:pk>/dispatch/', views.trip_dispatch, name='trip_dispatch'),
    path('trips/<int:pk>/complete/', views.trip_complete, name='trip_complete'),
    path('trips/<int:pk>/cancel/', views.trip_cancel, name='trip_cancel'),

    # Maintenance
    path('maintenance/', views.maintenance_list, name='maintenance_list'),
    path('maintenance/add/', views.maintenance_create, name='maintenance_create'),
    path('maintenance/<int:pk>/close/', views.maintenance_close, name='maintenance_close'),

    # Fuel Logs
    path('fuel-logs/', views.fuel_log_list, name='fuel_log_list'),
    path('fuel-logs/add/', views.fuel_log_create, name='fuel_log_create'),

    # Reports
    path('reports/', views.reports, name='reports'),

    # ==========================
    # Vehicle Documents
    # ==========================
    path(
        'documents/',
        views.vehicle_document_list,
        name='vehicle_document_list'
    ),

    path(
        'documents/add/',
        views.vehicle_document_create,
        name='vehicle_document_create'
    ),
]
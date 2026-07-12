from django.contrib import admin
from .models import Vehicle, Driver, Trip, MaintenanceLog, FuelLog, Expense, VehicleDocument

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('registration_number', 'name_model', 'vehicle_type', 'status', 'region')
    list_filter = ('status', 'vehicle_type', 'region')
    search_fields = ('registration_number', 'name_model')

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ('name', 'license_number', 'license_expiry_date', 'status', 'safety_score')
    list_filter = ('status',)
    search_fields = ('name', 'license_number')

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ('source', 'destination', 'vehicle', 'driver', 'cargo_weight', 'status')
    list_filter = ('status',)

@admin.register(MaintenanceLog)
class MaintenanceLogAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'description', 'cost', 'status')
    list_filter = ('status',)

@admin.register(FuelLog)
class FuelLogAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'liters', 'cost', 'date')

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'expense_type', 'amount', 'date')
    list_filter = ('expense_type',)

@admin.register(VehicleDocument)
class VehicleDocumentAdmin(admin.ModelAdmin):
    list_display = (
        "vehicle",
        "document_type",
        "document_number",
        "expiry_date",
    )
    list_filter = ("document_type",)
    search_fields = (
        "vehicle__registration_number",
        "document_number",
    )
    
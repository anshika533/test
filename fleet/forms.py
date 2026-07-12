from django import forms
from .models import Vehicle, Driver, Trip, MaintenanceLog, FuelLog

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['registration_number', 'name_model', 'vehicle_type', 'max_load_capacity',
                  'odometer', 'acquisition_cost', 'region']

class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['name', 'license_number', 'license_category', 'license_expiry_date',
                  'contact_number', 'safety_score']
        widgets = {'license_expiry_date': forms.DateInput(attrs={'type': 'date'})}

class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['source', 'destination', 'vehicle', 'driver', 'cargo_weight', 'planned_distance']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['vehicle'].queryset = Vehicle.objects.filter(status='AVAILABLE')
        self.fields['driver'].queryset = Driver.objects.filter(status='AVAILABLE')

class MaintenanceForm(forms.ModelForm):
    class Meta:
        model = MaintenanceLog
        fields = ['vehicle', 'description', 'cost']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['vehicle'].queryset = Vehicle.objects.exclude(status__in=['RETIRED', 'IN_SHOP'])

class FuelLogForm(forms.ModelForm):
    class Meta:
        model = FuelLog
        fields = ['vehicle', 'liters', 'cost', 'date']
        widgets = {'date': forms.DateInput(attrs={'type': 'date'})}

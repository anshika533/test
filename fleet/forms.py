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
        fields = '__all__'

        widgets = {
            'vehicle': forms.Select(attrs={'class': 'form-select'}),
            'driver': forms.Select(attrs={'class': 'form-select'}),
            'source': forms.TextInput(attrs={'class': 'form-control'}),
            'destination': forms.TextInput(attrs={'class': 'form-control'}),
            'distance_km': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['vehicle'].queryset = Vehicle.objects.filter(status='AVAILABLE')
        self.fields['driver'].queryset = Driver.objects.filter(status='AVAILABLE')

class MaintenanceForm(forms.ModelForm):
    class Meta:
        model = MaintenanceLog
        fields = '__all__'
        widgets = {
            'vehicle': forms.Select(attrs={'class': 'form-select'}),
            'maintenance_type': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'cost': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '₹ Enter Cost'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['vehicle'].queryset = Vehicle.objects.exclude(status__in=['RETIRED', 'IN_SHOP'])

class FuelLogForm(forms.ModelForm):
    class Meta:
        model = FuelLog
        fields = ['vehicle', 'liters', 'cost', 'date']
        widgets = {'date': forms.DateInput(attrs={'type': 'date'})}

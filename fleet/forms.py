from django import forms
from .models import Vehicle, Driver, Trip, MaintenanceLog, FuelLog, VehicleDocument
import re

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['registration_number', 'name_model', 'vehicle_type', 'max_load_capacity',
                  'odometer', 'acquisition_cost', 'region']




class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = "__all__"

    def clean_contact_number(self):
        contact = self.cleaned_data.get("contact_number")

        if not re.fullmatch(r'^[6-9]\d{9}$', contact):
            raise forms.ValidationError(
                "Enter a valid 10-digit mobile number."
            )

        return contact

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
            'date': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                }
            ),
            'cost': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '₹ Enter Cost'
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3
                }
            ),
            'status': forms.Select(
                attrs={'class': 'form-select'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

       
        self.fields['vehicle'].queryset = Vehicle.objects.filter(
            status='AVAILABLE'
        )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['vehicle'].queryset = Vehicle.objects.exclude(status__in=['RETIRED', 'IN_SHOP'])

class FuelLogForm(forms.ModelForm):
    class Meta:
        model = FuelLog
        fields = ['vehicle', 'liters', 'cost', 'date']
        widgets = {
            'vehicle': forms.Select(attrs={'class': 'form-select'}),
            'fuel_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'price_per_litre': forms.NumberInput(attrs={'class': 'form-control'}),
            'cost': forms.NumberInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class VehicleDocumentForm(forms.ModelForm):
    class Meta:
        model = VehicleDocument
        fields = "__all__"

        widgets = {
            "vehicle": forms.Select(attrs={"class": "form-select"}),
            "document_type": forms.Select(attrs={"class": "form-select"}),
            "document_number": forms.TextInput(attrs={"class": "form-control"}),
            "issue_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date"
                }
            ),
            "expiry_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date"
                }
            ),
        }
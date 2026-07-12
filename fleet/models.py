from django.db import models

# Create your models here.
class Vehicle(models.Model):
    STATUS_CHOICES = [
        ('AVAILABLE', 'Available'),
        ('ON_TRIP', 'On Trip'),
        ('IN_SHOP', 'In Shop'),
        ('RETIRED', 'Retired'),
    ]
    registration_number = models.CharField(max_length=20, unique=True)
    name_model = models.CharField(max_length=100)
    vehicle_type = models.CharField(max_length=50)
    max_load_capacity = models.DecimalField(max_digits=10, decimal_places=2, help_text="in kg")
    odometer = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    acquisition_cost = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='AVAILABLE')
    region = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.registration_number} - {self.name_model}"


class Driver(models.Model):
    STATUS_CHOICES = [
        ('AVAILABLE', 'Available'),
        ('ON_TRIP', 'On Trip'),
        ('OFF_DUTY', 'Off Duty'),
        ('SUSPENDED', 'Suspended'),
    ]
    name = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50, unique=True)
    license_category = models.CharField(max_length=50)
    license_expiry_date = models.DateField()
    contact_number = models.CharField(max_length=15)
    safety_score = models.DecimalField(max_digits=5, decimal_places=2, default=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='AVAILABLE')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def is_license_valid(self):
        from django.utils import timezone
        return self.license_expiry_date >= timezone.now().date()


class Trip(models.Model):
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('DISPATCHED', 'Dispatched'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    source = models.CharField(max_length=150)
    destination = models.CharField(max_length=150)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT, related_name='trips')
    driver = models.ForeignKey(Driver, on_delete=models.PROTECT, related_name='trips')
    cargo_weight = models.DecimalField(max_digits=10, decimal_places=2)
    planned_distance = models.DecimalField(max_digits=10, decimal_places=2)
    final_odometer = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    fuel_consumed = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    created_at = models.DateTimeField(auto_now_add=True)
    dispatched_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.source} -> {self.destination} ({self.status})"


class MaintenanceLog(models.Model):
    STATUS_CHOICES = [('OPEN', 'Open'), ('CLOSED', 'Closed')]
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='maintenance_logs')
    description = models.CharField(max_length=255)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPEN')
    created_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.vehicle} - {self.description}"


class FuelLog(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='fuel_logs')
    liters = models.DecimalField(max_digits=10, decimal_places=2)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    def __str__(self):
        return f"{self.vehicle} - {self.date} - {self.liters}L"


class Expense(models.Model):
    EXPENSE_TYPE = [('TOLL', 'Toll'), ('MAINTENANCE', 'Maintenance'), ('OTHER', 'Other')]
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='expenses')
    expense_type = models.CharField(max_length=20, choices=EXPENSE_TYPE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    note = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.vehicle} - {self.expense_type} - {self.amount}"
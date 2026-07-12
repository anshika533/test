from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Sum
from .models import Vehicle, Driver, Trip, MaintenanceLog, FuelLog, Expense
from .forms import VehicleForm, DriverForm, TripForm, MaintenanceForm, FuelLogForm


@login_required
def dashboard(request):
    vehicles = Vehicle.objects.all()
    vtype = request.GET.get('vehicle_type')
    status = request.GET.get('status')
    region = request.GET.get('region')

    if vtype:
        vehicles = vehicles.filter(vehicle_type=vtype)
    if status:
        vehicles = vehicles.filter(status=status)
    if region:
        vehicles = vehicles.filter(region=region)

    context = {
        'active_vehicles': vehicles.exclude(status='RETIRED').count(),
        'available_vehicles': vehicles.filter(status='AVAILABLE').count(),
        'vehicles_in_maintenance': vehicles.filter(status='IN_SHOP').count(),
        'active_trips': Trip.objects.filter(status='DISPATCHED').count(),
        'pending_trips': Trip.objects.filter(status='DRAFT').count(),
        'drivers_on_duty': Driver.objects.filter(status='ON_TRIP').count(),
        'total_vehicles': vehicles.count(),
        'vehicle_types': Vehicle.objects.values_list('vehicle_type', flat=True).distinct(),
        'regions': Vehicle.objects.exclude(region='').values_list('region', flat=True).distinct(),
        'status_counts': {
            'Available': vehicles.filter(status='AVAILABLE').count(),
            'On Trip': vehicles.filter(status='ON_TRIP').count(),
            'In Shop': vehicles.filter(status='IN_SHOP').count(),
            'Retired': Vehicle.objects.filter(status='RETIRED').count(),
        },
        'selected_type': vtype or '',
        'selected_status': status or '',
        'selected_region': region or '',
    }
    total = context['total_vehicles'] or 1
    context['fleet_utilization'] = round((context['active_trips'] / total) * 100, 1)
    return render(request, 'fleet/dashboard.html', context)


@login_required
def vehicle_list(request):
    vehicles = Vehicle.objects.exclude(status='RETIRED').order_by('registration_number')
    return render(request, 'fleet/vehicle_list.html', {'vehicles': vehicles})


@login_required
def vehicle_create(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vehicle registered successfully.')
            return redirect('vehicle_list')
    else:
        form = VehicleForm()
    return render(request, 'fleet/vehicle_form.html', {'form': form})


@login_required
def vehicle_edit(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    if request.method == 'POST':
        form = VehicleForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vehicle updated.')
            return redirect('vehicle_list')
    else:
        form = VehicleForm(instance=vehicle)
    return render(request, 'fleet/vehicle_form.html', {'form': form})


@login_required
def vehicle_delete(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    vehicle.status = 'RETIRED'
    vehicle.save()
    messages.success(request, 'Vehicle retired.')
    return redirect('vehicle_list')


@login_required
def driver_list(request):
    drivers = Driver.objects.all().order_by('name')
    return render(request, 'fleet/driver_list.html', {'drivers': drivers})


@login_required
def driver_create(request):
    if request.method == 'POST':
        form = DriverForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Driver added successfully.')
            return redirect('driver_list')
    else:
        form = DriverForm()
    return render(request, 'fleet/driver_form.html', {'form': form})


@login_required
def driver_edit(request, pk):
    driver = get_object_or_404(Driver, pk=pk)
    if request.method == 'POST':
        form = DriverForm(request.POST, instance=driver)
        if form.is_valid():
            form.save()
            messages.success(request, 'Driver updated.')
            return redirect('driver_list')
    else:
        form = DriverForm(instance=driver)
    return render(request, 'fleet/driver_form.html', {'form': form})


@login_required
def driver_delete(request, pk):
    driver = get_object_or_404(Driver, pk=pk)
    driver.delete()
    messages.success(request, 'Driver deleted.')
    return redirect('driver_list')


@login_required
def trip_list(request):
    trips = Trip.objects.all().order_by('-created_at')
    return render(request, 'fleet/trip_list.html', {'trips': trips})


@login_required
def trip_create(request):
    if request.method == 'POST':
        form = TripForm(request.POST)
        if form.is_valid():
            trip = form.save(commit=False)
            vehicle = trip.vehicle
            driver = trip.driver

            if trip.cargo_weight > vehicle.max_load_capacity:
                messages.error(request, f"Cargo weight exceeds {vehicle}'s max capacity.")
                return render(request, 'fleet/trip_form.html', {'form': form})

            if vehicle.status != 'AVAILABLE':
                messages.error(request, f"{vehicle} is not available (status: {vehicle.status}).")
                return render(request, 'fleet/trip_form.html', {'form': form})

            if driver.status != 'AVAILABLE':
                messages.error(request, f"{driver} is not available (status: {driver.status}).")
                return render(request, 'fleet/trip_form.html', {'form': form})
            if not driver.is_license_valid():
                messages.error(request, f"{driver}'s license has expired.")
                return render(request, 'fleet/trip_form.html', {'form': form})

            trip.status = 'DRAFT'
            trip.save()
            messages.success(request, 'Trip created as Draft.')
            return redirect('trip_list')
    else:
        form = TripForm()
    return render(request, 'fleet/trip_form.html', {'form': form})


@login_required
def trip_dispatch(request, pk):
    trip = get_object_or_404(Trip, pk=pk)
    if trip.status != 'DRAFT':
        messages.error(request, 'Only Draft trips can be dispatched.')
        return redirect('trip_list')
    trip.status = 'DISPATCHED'
    trip.dispatched_at = timezone.now()
    trip.save()
    trip.vehicle.status = 'ON_TRIP'
    trip.vehicle.save()
    trip.driver.status = 'ON_TRIP'
    trip.driver.save()
    messages.success(request, 'Trip dispatched.')
    return redirect('trip_list')


@login_required
def trip_complete(request, pk):
    trip = get_object_or_404(Trip, pk=pk)
    if trip.status != 'DISPATCHED':
        messages.error(request, 'Only Dispatched trips can be completed.')
        return redirect('trip_list')
    if request.method == 'POST':
        trip.final_odometer = request.POST.get('final_odometer') or trip.vehicle.odometer
        trip.fuel_consumed = request.POST.get('fuel_consumed') or 0
        trip.status = 'COMPLETED'
        trip.completed_at = timezone.now()
        trip.save()
        trip.vehicle.odometer = trip.final_odometer
        trip.vehicle.status = 'AVAILABLE'
        trip.vehicle.save()
        trip.driver.status = 'AVAILABLE'
        trip.driver.save()
        messages.success(request, 'Trip completed.')
        return redirect('trip_list')
    return render(request, 'fleet/trip_complete.html', {'trip': trip})


@login_required
def trip_cancel(request, pk):
    trip = get_object_or_404(Trip, pk=pk)
    if trip.status != 'DISPATCHED':
        messages.error(request, 'Only Dispatched trips can be cancelled.')
        return redirect('trip_list')
    trip.status = 'CANCELLED'
    trip.save()
    trip.vehicle.status = 'AVAILABLE'
    trip.vehicle.save()
    trip.driver.status = 'AVAILABLE'
    trip.driver.save()
    messages.success(request, 'Trip cancelled.')
    return redirect('trip_list')


@login_required
def maintenance_list(request):
    logs = MaintenanceLog.objects.all().order_by('-created_at')
    return render(request, 'fleet/maintenance_list.html', {'logs': logs})


@login_required
def maintenance_create(request):
    if request.method == 'POST':
        form = MaintenanceForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.status = 'OPEN'
            log.save()
            log.vehicle.status = 'IN_SHOP'
            log.vehicle.save()
            messages.success(request, 'Maintenance logged.')
            return redirect('maintenance_list')
    else:
        form = MaintenanceForm()
    return render(request, 'fleet/maintenance_form.html', {'form': form})


@login_required
def maintenance_close(request, pk):
    log = get_object_or_404(MaintenanceLog, pk=pk)
    if log.status == 'CLOSED':
        messages.error(request, 'Already closed.')
        return redirect('maintenance_list')
    log.status = 'CLOSED'
    log.closed_at = timezone.now()
    log.save()
    if log.vehicle.status != 'RETIRED':
        log.vehicle.status = 'AVAILABLE'
        log.vehicle.save()
    messages.success(request, 'Maintenance closed.')
    return redirect('maintenance_list')


@login_required
def fuel_log_create(request):
    if request.method == 'POST':
        form = FuelLogForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fuel log recorded.')
            return redirect('fuel_log_list')
    else:
        form = FuelLogForm()
    return render(request, 'fleet/fuel_log_form.html', {'form': form})


@login_required
def fuel_log_list(request):
    logs = FuelLog.objects.select_related('vehicle').order_by('-date')
    return render(request, 'fleet/fuel_log_list.html', {'logs': logs})


@login_required
def reports(request):
    vehicles = Vehicle.objects.all()
    data = []
    for v in vehicles:
        total_fuel_cost = v.fuel_logs.aggregate(s=Sum('cost'))['s'] or 0
        total_maint_cost = v.maintenance_logs.aggregate(s=Sum('cost'))['s'] or 0
        operational_cost = total_fuel_cost + total_maint_cost
        data.append({
            'vehicle': v, 'fuel_cost': total_fuel_cost,
            'maintenance_cost': total_maint_cost, 'operational_cost': operational_cost,
        })
    return render(request, 'fleet/reports.html', {'data': data})
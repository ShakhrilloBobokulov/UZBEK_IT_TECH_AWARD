from django.contrib.auth.models import User
from django.db import models
from localflavor.us.models import USPostalCodeField, USSocialSecurityNumberField, USStateField, USZipCodeField

# Create your models here.
class Company(models.Model):
    title = models.CharField(max_length=60, help_text="Company name")
    address = models.CharField(max_length=100, help_text="Address")
    taxnum = models.CharField(max_length=9)
    accnum = models.CharField(max_length=25)
    phonenum = models.CharField(blank=True, null=True, max_length=9)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return "%s" % (self.title)


class Vehicles(models.Model):
    title = models.CharField(max_length=50)
    def __str__(self):
        return self.title


class Rpmsettings(models.Model):
    vtype = models.ForeignKey(Vehicles, on_delete=models.CASCADE)
    cashfrom = models.IntegerField(blank=True, null=True)
    cashtill = models.IntegerField(blank=True, null=True)
    rpmfrom = models.FloatField(blank=True, null=True)
    rpmtill = models.FloatField(blank=True, null=True)
    cashdaily = models.IntegerField()
    bonus = models.FloatField()
    order = models.IntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return "%s (%s)" % (self.vtype, self.bonus)


class Dispatch(models.Model):
    fullname = models.CharField(max_length=60, help_text="Fullname")
    username = models.CharField(max_length=60, help_text="Username")
    telegramusername = models.CharField(max_length=50, blank=True, null=True)
    phonenum = models.CharField(blank=True, null=True, max_length=9)
    email = models.EmailField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return "%s (%s)" % (self.username, self.fullname)


class Trucks(models.Model):
    # added = models.ForeignKey('User', on_delete=models.PROTECT)
    unit = models.CharField(max_length=20, help_text="Unit name", unique=True)
    status = models.BooleanField(default=True, )
    companyowned = models.BooleanField(default=True, )
    # division = models.ForeignKey('Company', on_delete=models.PROTECT)
    trtype = models.ForeignKey('Vehicles', on_delete=models.PROTECT, blank=True, null=True)
    info = models.TextField(help_text="Info", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.unit


class Loads(models.Model):
    no = models.CharField(max_length=20, help_text="Loads No.", unique=True)
    truck = models.ForeignKey('Trucks', on_delete=models.PROTECT)
    dispatch = models.ForeignKey('Dispatch', on_delete=models.PROTECT)
    pickupstate = USStateField(blank=True)
    pickupzip = USZipCodeField(blank=True)
    droppstate = USStateField(blank=True)
    dropzip = USZipCodeField(blank=True)
    pickupdate = models.DateField()
    pickuptime = models.TimeField()
    dropdate = models.DateField()
    droptime = models.TimeField()
    trtype = models.ForeignKey(Vehicles, on_delete=models.PROTECT)
    allmiles = models.FloatField()
    totalrate = models.FloatField()
    rate = models.FloatField()
    info = models.TextField(help_text="Info", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.no

class KPIClusterResults(models.Model):
    dispatch = models.ForeignKey('Dispatch', on_delete=models.CASCADE)
    truck = models.ForeignKey('Trucks', on_delete=models.CASCADE)
    cluster_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Dispatch {self.dispatch.fullname} - Truck {self.truck.unit} - Cluster {self.cluster_id}"

class ForecastResults(models.Model):
    forecast_date = models.DateField()
    forecasted_demand = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Forecast for {self.forecast_date}: {self.forecasted_demand}"

class AnomalyResults(models.Model):
    load = models.ForeignKey('Loads', on_delete=models.CASCADE)
    totalrate = models.FloatField()
    allmiles = models.FloatField()
    is_anomaly = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Anomaly in Load ID {self.load.no} with Rate {self.totalrate}"
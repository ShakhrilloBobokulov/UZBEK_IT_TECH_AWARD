from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db.models import TimeField
from django.forms import DateTimeField

from visit.models import *
import re
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.contrib.auth.models import User
import datetime

from .models import *


class DateInput(forms.DateInput):
    input_type = "date"


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", widget=forms.TextInput(
        attrs={'class': 'form-control form-control-lg', 'autocomplete': 'off'}))
    password = forms.CharField(label="Password",
                               widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg'}))


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label="Username", widget=forms.TextInput(
        attrs={'class': 'form-control', 'autofocus': None, 'autocomplete': "off"}))
    email = forms.EmailField(label="Email",
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'autocomplete': "off"}))
    password1 = forms.CharField(label="Password",
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': "off"}))
    password2 = forms.CharField(label="Repeat password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('title', 'address', 'taxnum', 'accnum', 'phonenum')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'taxnum': forms.TextInput(attrs={'class': 'form-control'}),
            'accnum': forms.TextInput(attrs={'class': 'form-control'}),
            'phonenum': forms.TextInput(attrs={'class': 'form-control'}, ),
        }
        labels = {
            'title': "Company name",
            'address': "Company address",
            'taxnum': "Tax number",
            'accnum': "Account number",
            'phonenum': "Phone number",
        }

class VehicletpyesForm(forms.ModelForm):
    class Meta:
        model = Vehicles
        # fields = ('telegramusername',)
        fields = ('title',)
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': "Type of vehicle",
        }

class RpmsettingsForm(forms.ModelForm):
    class Meta:
        model = Rpmsettings
        fields = ('vtype', 'cashfrom', 'cashtill', 'rpmfrom', 'rpmtill', 'cashdaily', 'bonus', 'order')
        widgets = {
            'vtype': forms.Select(
                attrs={'class': 'select', 'data-mdb-filter': 'true', 'data-mdb-clear-button': 'true',
                       'data-mdb-select-init': 'data-mdb-select-init'}),
            'cashfrom': forms.NumberInput(attrs={'class': 'form-control'}),
            'cashtill': forms.NumberInput(attrs={'class': 'form-control'}),
            'rpmfrom': forms.NumberInput(attrs={'class': 'form-control'}),
            'rpmtill': forms.NumberInput(attrs={'class': 'form-control'}),
            'cashdaily': forms.NumberInput(attrs={'class': 'form-control'}),
            'bonus': forms.NumberInput(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'vtype': "Vehicle type",
            'cashfrom': "Income from",
            'cashtill': "Income till",
            'rpmfrom': "RPM from",
            'rpmtill': "RPM till",
            'cashdaily': "Daily min. income",
            'bonus': "Bonus dispatch",
            'order': "Raw order",
        }

class DispatchForm(forms.ModelForm):
    class Meta:
        model = Dispatch
        fields = ('fullname', 'username', 'telegramusername', 'phonenum', 'email')
        widgets = {
            'fullname': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'telegramusername': forms.TextInput(attrs={'class': 'form-control'}),
            'phonenum': forms.TextInput(attrs={'class': 'form-control'}, ),
            'email': forms.EmailInput(attrs={'class': 'form-control'}, ),
        }
        labels = {
            'fullname': "Fullname",
            'username': "Username",
            'telegramusername': "Telegram nickname",
            'phonenum': "Phone num.",
            'email': "Email",
        }


class TrucksForm(forms.ModelForm):
    info = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'md-textarea form-control-sm form-control', 'rows': '6',
               'placeholder': 'Additional note info of truck'}), required=False)

    class Meta:
        model = Trucks
        fields = ('unit', 'status', 'companyowned', 'trtype', 'info')
        widgets = {
            'trtype': forms.Select(
                attrs={'class': 'select', 'data-mdb-filter': 'true', 'data-mdb-clear-button': 'true',
                       'data-mdb-select-init': 'data-mdb-select-init'}),
            'unit': forms.TextInput(attrs={'class': 'form-control'}),

        }
        labels = {
            'unit': "Unit",
            'companyowned': "Company owned?",
            'status': "Active",
            'trtype': "Type of truck",
            'info': "Info about truck",
        }


class LoadsForm(forms.ModelForm):
    info = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'md-textarea form-control-sm form-control', 'rows': '6',
               'placeholder': 'Additional note info of truck'}), required=False)

    class Meta:
        model = Loads
        fields = (
            'no', 'truck', 'dispatch', 'pickupstate', 'pickupzip', 'droppstate', 'dropzip', 'pickupdate', 'pickuptime',
            'dropdate', 'droptime', 'trtype', 'allmiles', 'totalrate', 'rate', 'info')
        widgets = {
            'no': forms.TextInput(attrs={'class': 'form-control'}),
            'truck': forms.Select(
                attrs={'class': 'select', 'data-mdb-filter': 'true', 'data-mdb-clear-button': 'true',
                       'data-mdb-select-init': 'data-mdb-select-init'}),
            'trtype': forms.Select(
                attrs={'class': 'select', 'data-mdb-filter': 'true', 'data-mdb-clear-button': 'true',
                       'data-mdb-select-init': 'data-mdb-select-init'}),
            'dispatch': forms.Select(
                attrs={'class': 'select', 'data-mdb-filter': 'true', 'data-mdb-clear-button': 'true',
                       'data-mdb-select-init': 'data-mdb-select-init'}),
            'pickupstate': forms.Select(
                attrs={'class': 'select', 'data-mdb-filter': 'true', 'data-mdb-clear-button': 'true',
                       'data-mdb-select-init': 'data-mdb-select-init'}),
            'droppstate': forms.Select(
                attrs={'class': 'select', 'data-mdb-filter': 'true', 'data-mdb-clear-button': 'true',
                       'data-mdb-select-init': 'data-mdb-select-init'}),
            'pickupdate': forms.DateInput(
                attrs={'class': 'form-control', 'data-mdb-toggle': "datepicker"}),
            'pickuptime': forms.TimeInput(
                attrs={'class': 'form-control', 'data-mdb-toggle': "timepicker"}),
            'dropdate': forms.DateInput(
                attrs={'class': 'form-control', 'data-mdb-toggle': "datepicker"}),
            'droptime': forms.TimeInput(
                attrs={'class': 'form-control', 'data-mdb-toggle': "timepicker"}),
            'allmiles': forms.NumberInput(attrs={'class': 'form-control'}),
            'totalrate': forms.NumberInput(attrs={'class': 'form-control'}),
            'rate': forms.NumberInput(attrs={'class': 'form-control'}),

        }
        labels = {
            'no': 'Load No',
            'truck': 'Truck',
            'dispatch': 'Dispatcher',
            'pickupstate': 'Pick up State',
            'pickupzip': 'Pick up zip code',
            'droppstate': 'Drop state',
            'dropzip': 'Drop zip code',
            'pickupdate': 'Pick up date',
            'pickuptime': 'Pick up time[23:45]',
            'dropdate': 'Drop date',
            'droptime': 'Drop time[23:45]',
            'trtype': 'Truck type',
            'allmiles': 'All miles',
            'totalrate': 'Total amount',
            'rate': "Rate",
            'info': 'Info'
        }



class KPIClusteringForm(forms.Form):
    # Parameters for clustering, such as the number of clusters
    num_clusters = forms.IntegerField(initial=3, widget=forms.NumberInput(attrs={'class': 'form-control'}),  help_text="Number of clusters to form.")


class ForecastForm(forms.Form):
    # You may add necessary fields here, e.g., parameters to refine the forecast model
    start_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'data-mdb-toggle': "datepicker"}),help_text="Optional: Start date for historical data.")
    end_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'data-mdb-toggle': "datepicker"}), help_text="Optional: End date for historical data.")

class VisualizationForm(forms.Form):
    # Fields for selecting what kind of visualization to generate can be added
    metric_choice = forms.ChoiceField(choices=[('totalrate', 'Total Rate'), ('allmiles', 'All Miles')], required=True, help_text="Select a metric to visualize.")


class AnomalyDetectionForm(forms.Form):
    # Parameters for anomaly detection could be added here if needed
    contamination = forms.FloatField(initial=0.1, widget=forms.NumberInput(attrs={'class': 'form-control'}), help_text="Proportion of anomalies in the data.")

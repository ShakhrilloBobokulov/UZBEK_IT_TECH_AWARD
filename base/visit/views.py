from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from .forms import *
from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from django.contrib import messages
from .decorators import *
from django.utils.decorators import method_decorator
from django.utils.dateparse import parse_date
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest
import plotly.graph_objects as go
import plotly.express as px
from plotly.offline import plot

import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
import io
import urllib, base64


# Create your views here.
def index(request):
    return render(request, 'visit/main.html', {'title': 'Metrics UP'})


@unauthenticated_user
def user_login(request):
    title = "User Login"
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Authorization accepted')
            return redirect('homepage')
        else:
            messages.error(request, 'Authorization failed(Username or password is wrong)')
    else:
        form = UserLoginForm()
    return render(request, 'visit/login.html', {
        'form': form,
        'title': title
    })


@authenticated_user
def user_logout(request):
    logout(request)
    return redirect('homepage')


@unauthenticated_user
def register(request):
    title = "User Registration"
    form = UserRegisterForm(request.POST)
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration accepted')
            return redirect('login')
        else:
            messages.error(request, 'Failed with registration')
    else:
        form = UserRegisterForm()

    return render(request, 'visit/register.html', {
        'form': form,
        'title': title
    })


def video(request):
    return render(request, 'visit/video.html', {'title': 'Metrics UP'})


def faq(request):
    return render(request, 'visit/faq.html', {'title': 'Metrics UP'})


def blog(request):
    return render(request, 'visit/blog.html', {'title': 'Metrics UP'})


def opinions(request):
    return render(request, 'visit/opinions.html', {'title': 'Metrics UP'})





# @adminallow
def adminmain(request):
    return render(request, 'adminpage/main.html', {'title': 'Metrics UP'})


def admuserp(request):
    title = "User profile "
    return render(request, 'adminpage/user/userprofile.html', {
        'title': title
    })

def admcompdet(request):
    title = "Company details"
    # company = Company.objects.filter(user=request.user)
    company = Company.objects.all()
    if company:
        company = company.first()
    return render(request, 'adminpage/company/detail.html', {
        'title': title,
        'company': company
    })


def admcompadd(request):
    title = "Add company details"
    if request.method == 'POST':
        companyinfo = CompanyForm(request.POST)
        if companyinfo.is_valid():
            companyinfo = companyinfo.save(False)
            companyinfo.user = request.user
            companyinfo.save()

            messages.success(request, "Company info is added successfully")
            return redirect('admcompdet', )
        else:
            messages.error(request, "Problem with adding company info")
    else:
        companyinfo = CompanyForm()
    # return render(request, 'adminpage/vehicles/add.html', {'title': ''})
    return render(request, 'adminpage/company/add.html', {
        'title': title,
        'companyinfo': companyinfo,
    })

def admcompupd(request, pk):
    companymodel = get_object_or_404(Company, pk=pk)
    companyinfo = CompanyForm(request.POST or None, instance=companymodel)
    if companyinfo.is_valid():
        companyinfo.save()

        messages.success(request, "Comapny info is updated")
        return redirect('admcompdet', )

    title = "Update Company info"
    return render(request, 'adminpage/company/update.html', {
        'title': title,
        'companyinfo': companyinfo,
        'companymodel': companymodel,
    })

def admtypevehicleslist(request):
    title = "Vehicle types list"
    vehicletypelist = Vehicles.objects.all()
    return render(request, 'adminpage/vehicles/list.html', {
        'title': title,
        'vehicletypelist': vehicletypelist,
    })

def admtypevehicleadd(request):
    title = "Add new type of vehicle"
    if request.method == 'POST':
        vehicletype = VehicletpyesForm(request.POST)
        if vehicletype.is_valid():
            vehicletype = vehicletype.save()
            messages.success(request, "New vehcile type is added")
            return redirect('admtypevehicles', )
        else:
            messages.error(request, "Problem with adding new vehicle type")
    else:
        vehicletype = VehicletpyesForm()
    # return render(request, 'adminpage/vehicles/add.html', {'title': ''})
    return render(request, 'adminpage/vehicles/add.html', {
        'title': title,
        'vehicletype': vehicletype,
    })


class Detailtypevehicle(DetailView, LoginRequiredMixin):
    model = Vehicles
    template_name = 'adminpage/vehicles/detail.html'
    context_object_name = 'vehicletypeinfo'

    # pk_url_kwarg = 'pk'
    def get_object(self):
        id_ = self.kwargs.get('pk')
        owner = get_object_or_404(Vehicles, id=id_)
        return owner
        # if iftapm.truck.division in self.request.user.usersinfo.company.all():
        #     return iftapm
        # else:
        #     raise Http404()

    def get_context_data(self, *, object_list=None, **kwargs):
        # context = super(HomeNews, self).get_context_data()
        context = super().get_context_data(**kwargs)
        context['title'] = "Vehicle type info"
        # context['now'] = datetime.date.today()
        return context


def admtypevehicleupd(request, pk):
    tvehiclemodel = get_object_or_404(Vehicles, pk=pk)

    vehicletype = VehicletpyesForm(request.POST or None, instance=tvehiclemodel)

    if vehicletype.is_valid():
        vehicletype.save()

        messages.success(request, "Vehcile type info is updated")
        return redirect('admtypevehicleview', tvehiclemodel.pk)

    title = "Update vehicle info"
    return render(request, 'adminpage/vehicles/update.html', {
        'title': title,
        'tvehiclemodel': tvehiclemodel,
        'vehicletype': vehicletype,
    })


def admtypevehicledel(request, pk):
    title = "Delete vehicle type info"
    tvehiclemodel = get_object_or_404(Vehicles, pk=pk)

    if request.method == 'POST':
        tvehiclemodel.delete()
        messages.success(request, "Vehcile type info is deleted succesfully")
        return redirect('admtypevehicles')

    return render(request, 'adminpage/vehicles/delete.html', {'title': title, 'tvehiclemodel': tvehiclemodel})





# RPM CRUD
def admrpmsetlist(request):
    title = "RPM setting list"
    rpmsettinglist = Rpmsettings.objects.all()
    return render(request, 'adminpage/rpmset/list.html', {
        'title': title,
        'rpmsettinglist': rpmsettinglist,
    })


def admrpmsetadd(request):
    title = "Add new RPM setting"
    if request.method == 'POST':
        rpmsetting = RpmsettingsForm(request.POST)
        if rpmsetting.is_valid():
            rpmsetting = rpmsetting.save()
            messages.success(request, "New RPM setting is added")
            return redirect('admrpmsetlist', )
        else:
            messages.error(request, "Problem with adding new RPM setting")
    else:
        rpmsetting = RpmsettingsForm()
    return render(request, 'adminpage/rpmset/add.html', {
        'title': title,
        'rpmsetting': rpmsetting,
    })


class Detailrpmset(DetailView, LoginRequiredMixin):
    model = Rpmsettings
    template_name = 'adminpage/rpmset/detail.html'
    context_object_name = 'rpmsetinfo'

    # pk_url_kwarg = 'pk'
    def get_object(self):
        id_ = self.kwargs.get('pk')
        obj = get_object_or_404(Rpmsettings, id=id_)
        return obj

    def get_context_data(self, *, object_list=None, **kwargs):
        # context = super(HomeNews, self).get_context_data()
        context = super().get_context_data(**kwargs)
        context['title'] = "RPM setting info"
        # context['now'] = datetime.date.today()
        return context


def admrpmsetupd(request, pk):
    rpmsettingmodel = get_object_or_404(Rpmsettings, pk=pk)
    rpmsetting = RpmsettingsForm(request.POST or None, instance=rpmsettingmodel)

    if rpmsetting.is_valid():
        rpmsetting.save()

        messages.success(request, "RPM setting info is updated")
        return redirect('admrpmsetview', rpmsettingmodel.pk)

    title = "Update RPM setting info"
    return render(request, 'adminpage/rpmset/update.html', {
        'title': title,
        'rpmsettingmodel': rpmsettingmodel,
        'rpmsetting': rpmsetting,
    })


def admrpmsetdel(request, pk):
    title = "Delete RPM setting info"
    rpmsetmodel = get_object_or_404(Rpmsettings, pk=pk)

    if request.method == 'POST':
        rpmsetmodel.delete()
        messages.success(request, "RPM setting info is deleted succesfully")
        return redirect('admrpmsetlist')

    return render(request, 'adminpage/rpmset/delete.html', {'title': title, 'rpmsetmodel': rpmsetmodel})
# RPM CRUD



# dispatcher CRUD
def admdisplist(request):
    title = "Dispatchers list"
    displist = Dispatch.objects.all()
    return render(request, 'adminpage/disp/list.html', {
        'title': title,
        'displist': displist,
    })



def admdispadd(request):
    title = "Add new Dispatcher"
    if request.method == 'POST':
        disp = DispatchForm(request.POST)
        if disp.is_valid():
            disp = disp.save()
            messages.success(request, "New Dispatcher is added")
            return redirect('admdisplist', )
        else:
            messages.error(request, "Problem with adding new Dispatcher")
    else:
        disp = DispatchForm()
    return render(request, 'adminpage/disp/add.html', {
        'title': title,
        'disp': disp,
    })


class Detaildisp(DetailView, LoginRequiredMixin):
    model = Dispatch
    template_name = 'adminpage/disp/detail.html'
    context_object_name = 'dispinfo'

    # pk_url_kwarg = 'pk'
    def get_object(self):
        id_ = self.kwargs.get('pk')
        obj = get_object_or_404(Dispatch, id=id_)
        return obj

    def get_context_data(self, *, object_list=None, **kwargs):
        # context = super(HomeNews, self).get_context_data()
        context = super().get_context_data(**kwargs)
        context['title'] = "Dispatcher info"
        # context['now'] = datetime.date.today()
        return context



def admdispupd(request, pk):
    dispmodel = get_object_or_404(Dispatch, pk=pk)
    disp = DispatchForm(request.POST or None, instance=dispmodel)

    if disp.is_valid():
        disp.save()
        messages.success(request, "Dispatcher info is updated")
        return redirect('admdispview', dispmodel.pk)

    title = "Update Dispathcer info"
    return render(request, 'adminpage/disp/update.html', {
        'title': title,
        'dispmodel': dispmodel,
        'disp': disp,
    })



def admdispdel(request, pk):
    title = "Delete Dispatcher info"
    dispmodel = get_object_or_404(Dispatch, pk=pk)

    if request.method == 'POST':
        dispmodel.delete()
        messages.success(request, "Dispatcher info is deleted succesfully")
        return redirect('admdisplist')

    return render(request, 'adminpage/disp/delete.html', {'title': title, 'dispmodel': dispmodel})
# dispatcher CRUD



# truck CRUD
def admtrucklist(request):
    title = "Trucks list"
    trucklist = Trucks.objects.all()
    return render(request, 'adminpage/truck/list.html', {
        'title': title,
        'trucklist': trucklist,
    })


def admtruckadd(request):
    title = "Add new Truck"
    if request.method == 'POST':
        truck = TrucksForm(request.POST)
        if truck.is_valid():
            truck = truck.save()
            messages.success(request, "New Truck is added")
            return redirect('admtrucklist', )
        else:
            messages.error(request, "Problem with adding new Truck")
    else:
        truck = TrucksForm()
    return render(request, 'adminpage/truck/add.html', {
        'title': title,
        'truck': truck,
    })


class Detailtruck(DetailView, LoginRequiredMixin):
    model = Trucks
    template_name = 'adminpage/truck/detail.html'
    context_object_name = 'truckinfo'

    # pk_url_kwarg = 'pk'
    def get_object(self):
        id_ = self.kwargs.get('pk')
        obj = get_object_or_404(Trucks, id=id_)
        return obj

    def get_context_data(self, *, object_list=None, **kwargs):
        # context = super(HomeNews, self).get_context_data()
        context = super().get_context_data(**kwargs)
        context['title'] = "Truck info"
        # context['now'] = datetime.date.today()
        return context


def admtruckupd(request, pk):
    truckmodel = get_object_or_404(Trucks, pk=pk)
    truck = TrucksForm(request.POST or None, instance=truckmodel)

    if truck.is_valid():
        truck.save()
        messages.success(request, "Truck info is updated")
        return redirect('admtruckview', truckmodel.pk)

    title = "Update Truck info"
    return render(request, 'adminpage/truck/update.html', {
        'title': title,
        'truckmodel': truckmodel,
        'truck': truck,
    })


def admtruckdel(request, pk):
    title = "Delete Truck info"
    truckmodel = get_object_or_404(Trucks, pk=pk)

    if request.method == 'POST':
        truckmodel.delete()
        messages.success(request, "Truck info is deleted succesfully")
        return redirect('admtrucklist')

    return render(request, 'adminpage/truck/delete.html', {'title': title, 'truckmodel': truckmodel})

# truck CRUD


# loads CRUD
def admloadslist(request):
    title = "Loads management"
    loads = Loads.objects.all()
    return render(request, 'adminpage/loads/list.html', {
        'title': title,
        'loads': loads,
    })


def admloadsadd(request):
    title = "Add new Load info"
    if request.method == 'POST':
        loads = LoadsForm(request.POST)
        if loads.is_valid():
            loads = loads.save()
            messages.success(request, "New Load is added")
            return redirect('admloadslist', )
        else:
            messages.error(request, "Problem with adding new Load")
    else:
        loads = LoadsForm()
    return render(request, 'adminpage/loads/add.html', {
        'title': title,
        'loads': loads,
    })


class Detailload(DetailView, LoginRequiredMixin):
    model = Loads
    template_name = 'adminpage/loads/detail.html'
    context_object_name = 'loadinfo'

    # pk_url_kwarg = 'pk'
    def get_object(self):
        id_ = self.kwargs.get('pk')
        obj = get_object_or_404(Loads, id=id_)
        return obj

    def get_context_data(self, *, object_list=None, **kwargs):
        # context = super(HomeNews, self).get_context_data()
        context = super().get_context_data(**kwargs)
        context['title'] = "Load info"
        # context['now'] = datetime.date.today()
        return context


def admloadupd(request, pk):
    loadmodel = get_object_or_404(Loads, pk=pk)
    loads = LoadsForm(request.POST or None, instance=loadmodel)

    if loads.is_valid():
        loads.save()
        messages.success(request, "Load info is updated")
        return redirect('admloadview', loadmodel.pk)
    title = "Update Load info"
    return render(request, 'adminpage/loads/update.html', {
        'title': title,
        'loadmodel': loadmodel,
        'loads': loads,
    })


def admloaddel(request, pk):
    title = "Delete Load info"
    loadmodel = get_object_or_404(Loads, pk=pk)

    if request.method == 'POST':
        loadmodel.delete()
        messages.success(request, "Load info is deleted succesfully")
        return redirect('admloadslist')

    return render(request, 'adminpage/loads/delete.html', {'title': title, 'loadmodel': loadmodel})

# loads CRUD



# KPI MANAGEMENT
def kpi_clustering_dashboard(request):
    """Dashboard for KPI clustering"""
    title = "KPI Clustering"
    form = KPIClusteringForm()
    return render(request, 'adminpage/kpi/dashboard.html', {
        'form': form,
        'title': title
    })


def kpi_analysis_form(request):
    # Preset the form with the current week's date range
    title = "KPI Optimization"
    default_start_date = datetime.today() - timedelta(days=7)  # Adjusting to use datetime class
    default_end_date = datetime.today()  # Use datetime for the current date

    if request.method == 'GET':
        start_date = request.GET.get('start_date', default_start_date).date()  # Ensure it's a date object
        end_date = request.GET.get('end_date', default_end_date).date()  # Ensure it's a date object

    # Render the form template
    return render(request, 'adminpage/kpi/kpi_analysis_form.html', {
        'start_date': start_date,
        'end_date': end_date,
        'title': title
    })



def kpi_analysis(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    title = "KPI optimization"

    # Ensure dates are provided
    if not start_date or not end_date:
        return render(request, 'error.html', {'message': 'Please provide start and end dates.'})

    # Parse the dates
    start_date = parse_date(start_date)
    end_date = parse_date(end_date)

    # Retrieve loads data for the specified date range
    loads_data = Loads.objects.select_related('truck', 'dispatch').filter(pickupdate__range=(start_date, end_date))
    rpm_data = Rpmsettings.objects.select_related('vtype').all()

    # Create DataFrames from the queryset
    loads_df = pd.DataFrame(
        list(loads_data.values('no', 'truck__id', 'dispatch_id', 'pickupdate', 'totalrate', 'allmiles'))
    )

    # Calculate load rate
    loads_df['rate'] = loads_df['totalrate'] / loads_df['allmiles']

    # Create DataFrame for RPM settings
    rpm_df = pd.DataFrame(list(rpm_data.values('vtype_id', 'rpmfrom', 'rpmtill')))

    # Merge loads DataFrame with RPM settings on truck_id and vtype_id
    merged_data = pd.merge(loads_df, rpm_df, left_on='truck__id', right_on='vtype_id', how='left')

    # Initialize the Plotly figure
    fig = go.Figure()

    # Define the threshold for coloring
    rpm_threshold = 0.5  # Adjust this based on your criteria for performance evaluation

    # Add a line for each truck
    for truck_id in merged_data['truck__id'].unique():
        truck_data = merged_data[merged_data['truck__id'] == truck_id]

        # Adding lines and markers for load rates
        fig.add_trace(go.Scatter(
            x=truck_data['pickupdate'],  # Dates for x-axis
            y=truck_data['rate'],  # Load rate for y-axis
            mode='lines+markers',
            name=f'Truck {truck_id}',
            line=dict(width=2),  # Default line width
            marker=dict(size=8),
            hovertemplate=
            "Dispatcher: %{text}<br>" +
            "Truck No: %{name}<br>" +
            "Order No: %{customdata[0]}<br>" +
            "All Miles: %{customdata[1]}<br>" +
            "Total Rate: %{customdata[2]}<br>" +
            "<extra></extra>",
            text=truck_data['dispatch_id'],  # To show the dispatcher name
            customdata=truck_data[['no', 'allmiles', 'totalrate']].values.tolist(),  # Extra data for hover
        ))

        # Mark sections in red or green based on performance vs. RPM setting
        for i in range(len(truck_data) - 1):
            color = 'red' if truck_data['rate'].iloc[i] < truck_data['rpmfrom'].iloc[i] * (
                        1 - rpm_threshold / 100) else 'green'
            fig.add_trace(go.Scatter(
                x=truck_data['pickupdate'].iloc[i:i + 2],  # Two consecutive dates
                y=truck_data['rate'].iloc[i:i + 2],  # Corresponding rates
                mode='lines',
                line=dict(color=color, width=3),  # Color based on performance
                showlegend=False
            ))

    # Update layout for better visualization
    fig.update_layout(
        title='Truck Load Rates Over Time',
        xaxis_title='Date',
        yaxis_title='Load Rate',
        xaxis=dict(tickformat="%Y-%m-%d"),  # Set x-axis to show only date without time
        yaxis=dict(title='Rate'),
        showlegend=True
    )

    plot_div = plot(fig, output_type='div')

    # Generate recommendations based on performance
        # Merge dataframes on truck_id
    merged_data = pd.merge(loads_df, rpm_df, left_on='truck__id', right_on='vtype_id', how='inner')
    merged_data['rpmset'] = (merged_data['rpmfrom'] + merged_data['rpmtill']) / 2
    merged_data['bonus'] = (merged_data['rate'] / merged_data['rpmset'] - 1) * 100


    recommendations = []
    below_kpi = merged_data[merged_data['bonus'] < 1]
    for dispatch_id in below_kpi['dispatch_id'].unique():
        disp_data = below_kpi[below_kpi['dispatch_id'] == dispatch_id]
        trucks_to_change = disp_data[disp_data['bonus'] < 1]['truck__id'].unique().tolist()
        dispatch_name = Dispatch.objects.get(id=dispatch_id).fullname
        recommendations.append({
            'dispatcher': dispatch_name,
            'trucks_to_reassign': trucks_to_change,
            'note': f"Consider reassigning trucks {trucks_to_change} from Dispatcher {dispatch_name}"
        })

    # Render the final page with the plot and recommendations
    return render(request, 'adminpage/kpi/kpi_analysis.html', {
        'plot_div': plot_div,
        'recommendations': recommendations,
        'start_date': start_date,
        'end_date': end_date,
        'title': title
    })

    # def kpi_analysis(request):
#     start_date = request.GET.get('start_date')
#     end_date = request.GET.get('end_date')
#
#     if not start_date or not end_date:
#         return render(request, 'error.html', {'message': 'Please provide start and end dates.'})
#
#     start_date = parse_date(start_date)
#     end_date = parse_date(end_date)
#
#     # Filter the database query on the date range
#     loads_data = Loads.objects.select_related('truck', 'dispatch').filter(pickupdate__range=(start_date, end_date))
#     rpm_data = Rpmsettings.objects.select_related('vtype').all()
#
#     # Create DataFrames from the querysets
#     loads_df = pd.DataFrame(
#         list(loads_data.values('no', 'truck__id', 'dispatch_id', 'pickupdate', 'totalrate', 'allmiles')))
#     rpm_df = pd.DataFrame(list(rpm_data.values('vtype_id', 'rpmfrom', 'rpmtill')))
#
#     # Calculate rate as totalrate divided by allmiles
#     loads_df['rate'] = loads_df['totalrate'] / loads_df['allmiles']
#
#     # Merge dataframes on truck_id
#     merged_data = pd.merge(loads_df, rpm_df, left_on='truck__id', right_on='vtype_id', how='inner')
#     merged_data['rpmset'] = (merged_data['rpmfrom'] + merged_data['rpmtill']) / 2
#     merged_data['bonus'] = (merged_data['rate'] / merged_data['rpmset'] - 1) * 100
#
#     # Define color based on performance thresholds
#     def determine_color(row):
#         if row['bonus'] >= 5:  # Threshold for good performance
#             return 'green'
#         elif row['bonus'] < 1:  # Threshold for bad performance
#             return 'red'
#         else:
#             return 'yellow'
#
#     merged_data['color'] = merged_data.apply(determine_color, axis=1)
#
#     # Create line plot with Plotly
#     fig = px.line(
#         merged_data,
#         x='pickupdate',
#         y='totalrate',
#         color='truck__id',
#         line_group='truck__id',
#         title='Truck Income Over Time',
#         labels={'truck__id': 'Truck ID', 'totalrate': 'Total Income'},
#     )
#
#     # Add marker points and color-coded sections
#     for truck_id in merged_data['truck__id'].unique():
#         truck_data = merged_data[merged_data['truck__id'] == truck_id]
#         for i, row in truck_data.iterrows():
#             fig.add_scatter(
#                 x=[row['pickupdate']],
#                 y=[row['totalrate']],
#                 mode='markers+text',
#                 marker=dict(color=row['color'], size=10),
#                 text=f"Disp: {row['dispatch_id']} ({str(round(row['bonus'], 2))}%)",
#                 textposition='top center'
#             )
#
#     plot_div = plot(fig, output_type='div')
#
#     # Generate recommendations
#     recommendations = []
#     below_kpi = merged_data[merged_data['bonus'] < 1]
#     for dispatch_id in below_kpi['dispatch_id'].unique():
#         disp_data = below_kpi[below_kpi['dispatch_id'] == dispatch_id]
#         trucks_to_change = disp_data[disp_data['bonus'] < 1]['truck__id'].unique().tolist()
#         dispatch_name = Dispatch.objects.get(id=dispatch_id).fullname
#         recommendations.append({
#             'dispatcher': dispatch_name,
#             'trucks_to_reassign': trucks_to_change,
#             'note': f"Consider reassigning trucks {trucks_to_change} from Dispatcher {dispatch_name}"
#         })
#
#     return render(request, 'adminpage/kpi/kpi_analysis.html', {
#         'plot_div': plot_div,
#         'recommendations': recommendations,
#         'start_date': start_date,
#         'end_date': end_date
#     })

def run_kpi_clustering(request):
    """Run K-Means clustering on dispatchers and trucks based on KPIs"""
    if request.method == 'POST':
        form = KPIClusteringForm(request.POST)
        if form.is_valid():
            # Data Aggregation
            load_data = Loads.objects.all().values('dispatch_id', 'truck_id', 'totalrate', 'rate')
            dispatch_data = Dispatch.objects.all().values('id', 'fullname')
            truck_data = Trucks.objects.all().values('id', 'unit')

            # Transforming to DataFrames
            load_df = pd.DataFrame(load_data)
            # Merge data based on necessary keys - customized based on desired scheme
            kpi_data = load_df[["totalrate", "rate"]]

            # Clustering
            num_clusters = form.cleaned_data['num_clusters']
            kmeans = KMeans(n_clusters=num_clusters, random_state=0).fit(kpi_data)
            load_df['cluster'] = kmeans.labels_

            # Save Results
            for idx, row in load_df.iterrows():
                KPIClusterResults.objects.create(dispatch_id=row['dispatch_id'], truck_id=row['truck_id'],
                                                 cluster_id=row['cluster'])

            messages.success(request, 'KPI Clustering complete')
            return redirect('kpi_clustering_results')
    else:
        return redirect('kpi_clustering_dashboard')


def kpi_clustering_results(request):
    title = "KPI Clustering results"
    """Display results of the KPI clustering"""
    results = KPIClusterResults.objects.select_related('dispatch', 'truck')
    return render(request, 'adminpage/kpi/results.html', {
        'results': results,
        'title': title
    })
# KPI MANAGEMENT


def demand_forecasting(request):
    """Forecast rates per mile for the next 10 days based on the last month's loads."""

    # Calculate the date range for the past month
    end_date = datetime.now().date()
    start_date = end_date - pd.DateOffset(months=1)  # One month ago from today

    # Retrieve loads data from the past month
    loads_data = Loads.objects.filter(pickupdate__range=(start_date, end_date))

    if not loads_data:
        return render(request, 'error.html', {'message': 'No load data available for the past month.'})

    # Create DataFrame from the queryset
    loads_df = pd.DataFrame(list(loads_data.values('pickupdate', 'totalrate', 'allmiles')))

    # Calculate rate per mile
    loads_df['rate_per_mile'] = loads_df['totalrate'] / loads_df['allmiles']

    # Convert pickupdate to datetime and set as index
    loads_df['pickupdate'] = pd.to_datetime(loads_df['pickupdate'])
    loads_df.set_index('pickupdate', inplace=True)

    # Check if there are enough data points
    if len(loads_df) < 2:
        return render(request, 'error.html', {'message': 'Not enough data to perform forecasting.'})

    # Fit ARIMA model to the data
    model = ARIMA(loads_df['rate_per_mile'], order=(1, 1, 1))  # Adjust ARIMA parameters if necessary
    model_fit = model.fit()

    # Forecast for the next 10 days
    forecasted_values = model_fit.forecast(steps=10)

    # Prepare forecast data for rendering in a DataFrame
    future_dates = [end_date + timedelta(days=i) for i in range(1, 11)]  # Next 10 days
    forecast_df = pd.DataFrame({
        'Date': future_dates,
        'Forecasted Rate per Mile': forecasted_values
    })

    # Create a Plotly figure for visualization
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=forecast_df['Date'],
        y=forecast_df['Forecasted Rate per Mile'],
        mode='lines+markers',
        name='Forecasted Rate per Mile',
        line=dict(color='blue', width=2),
        marker=dict(size=8)
    ))

    # Update the layout of the figure
    fig.update_layout(
        title='Rate per Mile Forecast for Next 10 Days',
        xaxis_title='Date',
        yaxis_title='Rate per Mile',
        xaxis=dict(tickformat="%Y-%m-%d"),  # Show only dates
        yaxis=dict(title='Rate per Mile'),
        showlegend=True
    )

    plot_div = plot(fig, output_type='div')

    # Render the final page with the forecast data and plot
    return render(request, 'adminpage/forecasting/demand_forecasting.html', {
        'forecast_table': forecast_df.to_html(index=False),  # Convert DataFrame to HTML for rendering
        'plot_div': plot_div,
        'title': "Demand Forecasting for Rates per Mile"
    })

def visualizations_dashboard(request):
    """Display dashboard for data visualizations"""
    title = "Data Visualization"
    form = VisualizationForm()
    return render(request, 'adminpage/visual/dashboard.html', {
        'form': form,
        'title': title
    })


def render_visualizations(request):
    """Generate visualizations for data analytics"""
    title = "Data Visualization"
    if request.method == 'POST':
        form = VisualizationForm(request.POST)
        if form.is_valid():
            # Data Visualization with Seaborn
            load_data = Loads.objects.all().order_by('pickupdate').values('totalrate', 'allmiles', 'pickupdate')
            data = pd.DataFrame(load_data)

            # Generate a static visualization with Seaborn
            plt.figure(figsize=(10, 6))
            sns.barplot(x='pickupdate', y='totalrate', data=data)
            plt.title('Total Rate Over Time')

            # Encode the plot to display it in the template
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            image_base64 = base64.b64encode(buf.read()).decode('utf-8').replace('\n', '')

            # Dynamic Visualization with Plotly
            fig = px.line(data, x='pickupdate', y='totalrate', title='Interactive Plotly Visualization')
            plot_div = fig.to_html(full_html=False)

            return render(request, 'adminpage/visual/render.html', {'image_base64': image_base64, 'plot_div': plot_div})
    else:
        form = VisualizationForm()
        return render(request, 'adminpage/visual/dashboard.html', {
            'form': form,
            'title': title
        })



def anomaly_detection_dashboard(request):
    """Display dashboard for anomaly detection"""
    title = "Anomaly Detection"
    form = AnomalyDetectionForm()
    return render(request, 'adminpage/anomaly/dashboard.html', {
        'form': form,
        'title': title
    })


def run_anomaly_detection(request):
    """Run Isolation Forest anomaly detection on load data"""
    if request.method == 'POST':
        form = AnomalyDetectionForm(request.POST)
        if form.is_valid():
            # Data Selection and Preprocessing
            load_data = Loads.objects.all().values('id', 'totalrate', 'allmiles')  # Include 'id' to keep track of rows
            data = pd.DataFrame(load_data)

            # Ensure there's enough data for meaningful analysis
            if data.empty or len(data) < 2:
                messages.error(request, 'Not enough data for anomaly detection.')
                return redirect('anomaly_detection_dashboard')

            data_scaled = (data[['totalrate', 'allmiles']] - data[['totalrate', 'allmiles']].mean()) / data[
                ['totalrate', 'allmiles']].std()  # Normalizing specific columns

            # Anomaly Detection
            iso_forest = IsolationForest(contamination=0.1, random_state=42)
            data['anomaly'] = iso_forest.fit_predict(data_scaled)

            # Save Results
            anomalies = data[data['anomaly'] == -1]
            for _, row in anomalies.iterrows():
                AnomalyResults.objects.create(load_id=row['id'], totalrate=row['totalrate'],
                                              allmiles=row['allmiles'])

            messages.success(request, 'Anomaly Detection complete')
            return redirect('anomaly_detection_results')
    else:
        return redirect('anomaly_detection_dashboard')

def anomaly_detection_results(request):
    """Display results of the anomaly detection"""
    title = "Results Anomaly Detection"
    results = AnomalyResults.objects.select_related('load')
    return render(request, 'adminpage/anomaly/results.html', {
        'results': results,
        'title': title
    })
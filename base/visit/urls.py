from django.urls import path, include
from . import views
from .views import *

urlpatterns = [
    path('', views.index, name="homepage"),
    path('video/', views.video, name="video"),
    path('faq/', views.faq, name="faq"),
    path('blog/', views.blog, name="blog"),
    path('opinions/', views.opinions, name="opinions"),
    path('login/', views.user_login, name="login"),
    #
    path('register/', views.register, name="register"),
    path('logout/', views.user_logout, name="logout"),
    # path('logout/', views.user_logout, name="logout"),
    #
    path('adminmain/', views.adminmain, name="adminmain"),
    #
    path('admuserp/', views.admuserp, name="admuserp"),
    path('admcompdet/', views.admcompdet, name="admcompdet"),
    path('admcompadd/', views.admcompadd, name="admcompadd"),
    path('admcompupd/<int:pk>', views.admcompupd, name="admcompupd"),
    #
    path('admtypevehicles/', views.admtypevehicleslist, name="admtypevehicles"),
    path('adtypevehicle/', views.admtypevehicleadd, name="adtypevehicle"),
    path('admtypevehicleview/<int:pk>', Detailtypevehicle.as_view(), name="admtypevehicleview"),
    path('admtypevehicleupd/<int:pk>', views.admtypevehicleupd, name="admtypevehicleupd"),
    path('admtypevehicledel/<int:pk>', views.admtypevehicledel, name="admtypevehicledel"),
    #
    path('admrpmsetlist/', views.admrpmsetlist, name="admrpmsetlist"),
    path('admrpmsetadd/', views.admrpmsetadd, name="admrpmsetadd"),
    path('admrpmsetview/<int:pk>', Detailrpmset.as_view(), name="admrpmsetview"),
    path('admrpmsetupd/<int:pk>', views.admrpmsetupd, name="admrpmsetupd"),
    path('admrpmsetdel/<int:pk>', views.admrpmsetdel, name="admrpmsetdel"),
    #
    path('admdisplist/', views.admdisplist, name="admdisplist"),
    path('admdispadd/', views.admdispadd, name="admdispadd"),
    path('admdispview/<int:pk>', Detaildisp.as_view(), name="admdispview"),
    path('admdispupd/<int:pk>', views.admdispupd, name="admdispupd"),
    path('admdispdel/<int:pk>', views.admdispdel, name="admdispdel"),
    #
    path('admtrucklist/', views.admtrucklist, name="admtrucklist"),
    path('admtruckadd/', views.admtruckadd, name="admtruckadd"),
    path('admtruckview/<int:pk>', Detailtruck.as_view(), name="admtruckview"),
    path('admtruckupd/<int:pk>', views.admtruckupd, name="admtruckupd"),
    path('admtruckdel/<int:pk>', views.admtruckdel, name="admtruckdel"),
    #
    path('admloadslist/', views.admloadslist, name="admloadslist"),
    path('admloadsadd/', views.admloadsadd, name="admloadsadd"),
    path('admloadview/<int:pk>', Detailload.as_view(), name="admloadview"),
    path('admloadupd/<int:pk>', views.admloadupd, name="admloadupd"),
    path('admloaddel/<int:pk>', views.admloaddel, name="admloaddel"),

    path('kpi-clustering-form/', views.kpi_analysis_form, name='kpi_clustering_dashboard_form'),
    path('kpi-clustering/', views.kpi_analysis, name='kpi_clustering_dashboard'),
    # path('kpi-clustering/', views.kpi_clustering_dashboard, name='kpi_clustering_dashboard'),
    path('kpi-clustering/run/', views.run_kpi_clustering, name='run_kpi_clustering'),
    path('kpi-clustering/results/', views.kpi_clustering_results, name='kpi_clustering_results'),

    #
    path('forecasting_demand/', views.demand_forecasting, name='forecasting_demand'),

    path('visualizations/', views.visualizations_dashboard, name='visualizations_dashboard'),
    path('visualizations/render/', views.render_visualizations, name='render_visualizations'),

    # path('forecasting/', views.forecasting_dashboard, name='forecasting_dashboard'),
    # path('forecasting/run/', views.run_forecast, name='run_forecast'),
    # path('forecasting/results/', views.forecast_results, name='forecast_results'),
    #
    #
    path('anomaly-detection/', views.anomaly_detection_dashboard, name='anomaly_detection_dashboard'),
    path('anomaly-detection/run/', views.run_anomaly_detection, name='run_anomaly_detection'),
    path('anomaly-detection/results/', views.anomaly_detection_results, name='anomaly_detection_results'),
    #



    # path('test/', views.test, name="test"),
]

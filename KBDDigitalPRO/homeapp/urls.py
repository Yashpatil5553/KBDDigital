from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.login_page, name='login'),
    path('login/', views.login_page),
    path('home/', views.home, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('GLSApp/', include('GLSApp.urls')),


    # GLS Check-in system
    path('gls-checkin/', views.gls_checkin, name='gls_checkin'),  # Login page
    path('gls-checkin/form/', views.gls_checkin_form, name='gls_checkin_form'),  # Check-in step
    path('gls-checked-list/', views.gls_checked_list, name='gls_checked_list'),  # Admin list view
    path('gls-admitted-report/', views.gls_admitted_list, name='gls_admitted_report'),
    path('gls-scan/', views.gls_qr_scan, name='gls_qr_scan'),
    path('bulkupload/', views.bulk_upload_view, name='bulkupload'),
    path('bulk/', views.bulk, name='bulk'),
]

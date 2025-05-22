from django.urls import path
from . import views

urlpatterns = [
    path('gls-home/', views.gls_home, name='gls_home'),
    path('calculation/', views.calculation, name='calculation'),
    path('ist-calculation/', views.ist_calculation, name='ist_calculation'),
    path('sector-distribution/', views.sector_distribution_input, name='sector_distribution_input'),
    path('target-card-form/', views.target_card_form, name='target_card_form'),
    path('input-values/', views.enter_sga_ik_pp, name='input_values'),
    path('finish/', views.finish_target_card, name='finish_target_card'),
    path('download-target-card/', views.download_target_card, name='download_target_card'),
    path('download-target-data/', views.download_all_target_data, name='download_target_data'),
    path('tc-filled-list/', views.tc_filled_list, name='tc_filled_list'),
]

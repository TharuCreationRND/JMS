from django.urls import path
from . import views
from .views import chatbot_view

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('jobs/', views.job_list, name='job_list'), 
    path('jobs/report/', views.job_report, name='job_report'),
    path('jobs/add/', views.add_job, name='add_job'),
    path('breakdowns/', views.breakdown_list, name='breakdown_list'),
    path('breakdowns/report/', views.breakdown_report, name='breakdown_report'),
    path('borrow/', views.borrow_list, name='borrow_list'),
    path('borrow/report/', views.borrow_report, name='borrow_report'), 
    path('breakdowns/add/', views.add_breakdown, name='add_breakdown'),
    path('borrow/add/', views.add_borrow, name='add_borrow'),
    path('jobs/edit/<int:job_id>/', views.edit_job, name='edit_job'),
    path('jobs/delete/<int:job_id>/', views.delete_job, name='delete_job'),
    path('jobs/export/', views.export_job_excel, name='export_job_excel'),
    path('jobs/delete_selected/', views.delete_selected_jobs, name='delete_selected_jobs'),
    path('breakdowns/edit/<int:breakdown_id>/', views.edit_breakdown, name='edit_breakdown'),
    path('breakdowns/delete/<int:breakdown_id>/', views.delete_breakdown, name='delete_breakdown'),
    path('breakdowns/delete_selected/', views.delete_selected_breakdowns, name='delete_selected_breakdowns'),
    path('breakdowns/export/', views.export_breakdown_excel, name='export_breakdown_excel'),
    path('borrow/report/', views.borrow_report, name='borrow_report'),
    path('borrow/export/', views.export_borrow_excel, name='export_borrow_excel'),
    path('borrow/edit/<int:pk>/', views.edit_borrow, name='edit_borrow'),
    path('borrow/delete/<int:pk>/', views.delete_borrow, name='delete_borrow'),
    path('chatbot/', chatbot_view, name='chatbot'),
    path('backupplans/', views.backupplan_list, name='backupplan_list'),
    path('backupplans/add/', views.add_backupplan, name='add_backupplan'),
    path('backupplans/edit/<int:plan_id>/', views.edit_backupplan, name='edit_backupplan'),
    path('backupplans/delete/<int:plan_id>/', views.delete_backupplan, name='delete_backupplan'),
    path('backupplans/export/', views.export_backupplans_excel, name='export_backupplans_excel'),
    path('backupplans/delete-selected/', views.delete_selected_backupplans, name='delete_selected_backupplans'),



]

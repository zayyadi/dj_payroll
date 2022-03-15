from django.urls import path
from django.contrib.auth import views as auth_views

import payroll.views as views



urlpatterns = [
    path("login/", auth_views.LoginView.as_view(template_name="login.html"),name='login'),
    path("logout/", auth_views.LogoutView.as_view(template_name="logout.html"), name="logout"),
    path("register/", views.SignUp, name="signup"),
    path('', views.home, name='home'),
    path('dashboard/',views.dashboard, name='dashboard'),
    path('add-dept/', views.addDepartment, name="add-department"),
    path('add-grade/', views.addGrade, name="add-grade"),
    path('add-payroll/', views.addPayroll, name="add-payroll"),
    path('add-ed/', views.addEandD, name="add-EandD"),
    path('pdf/<int:pk>/', views.myview, name="pdf"),
    path('payslip/<int:pk>/', views.payslip, name="payslip"),
    path('updatepayroll/<int:pk>/', views.payrollUpdate, name="updatepayroll"),
]

 # path('addemployee/', views.addEmployee, name='addemployee'),
    # path('addpayroll/', views.addPayroll, name='addpayroll'),
    # path('payrolldashboard/', views.payrolldashboard, name='payrolldashboard'),
    # path('updatepayroll/<int:pk>/', views.updatepayroll, name='updatepayroll'),
    # path('deletepayroll/<int:pk>/', views.deletepayroll, name='deletepayroll'),
    # path('employeedashboard', views.employeedashboard, name='employeedashboard'),
    # path('updateemployee/<int:pk>/', views.updateemployee, name='updateemployee'),
    # path('deleteemployee/<int:pk>/', views.deleteemployee, name='deleteemployee'),

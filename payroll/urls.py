from django.urls import path

import payroll.views as views

from wkhtmltopdf.views import PDFTemplateView

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/',views.dashboard, name='dashboard'),
    path('add-dept/', views.addDepartment, name="add-department"),
    path('add-grade/', views.addGrade, name="add-grade"),
    path('add-payroll/', views.addPayroll, name="add-payroll"),
    path('add-ed/', views.addEandD, name="add-EandD"),
    path('pdf/<int:pk>/', views.myview, name="pdf"),
    path('payslip/<int:pk>/', views.payslip, name="payslip"),
    # path('pdf/',  PDFTemplateView.as_view(template_name='payslip_template.html'), name='pdf')
    path('updatepayroll/<int:pk>/', views.payrollUpdate, name="updatepayroll"),
    # path('employee-update/<int:pk>/', views.employeeUpdate, name="employee-update")
]

 # path('addemployee/', views.addEmployee, name='addemployee'),
    # path('addpayroll/', views.addPayroll, name='addpayroll'),
    # path('payrolldashboard/', views.payrolldashboard, name='payrolldashboard'),
    # path('updatepayroll/<int:pk>/', views.updatepayroll, name='updatepayroll'),
    # path('deletepayroll/<int:pk>/', views.deletepayroll, name='deletepayroll'),
    # path('employeedashboard', views.employeedashboard, name='employeedashboard'),
    # path('updateemployee/<int:pk>/', views.updateemployee, name='updateemployee'),
    # path('deleteemployee/<int:pk>/', views.deleteemployee, name='deleteemployee'),

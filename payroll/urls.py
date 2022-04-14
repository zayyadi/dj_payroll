from django.urls import path

import payroll.views as views



urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/',views.dashboard, name='dashboard'),
    path('add-dept/', views.addDepartment, name="add-department"),
    path('add-grade/', views.addGrade, name="add-grade"),
    path('add-employee/', views.CreateEmployee.as_view(), name="add-employee"),
    path('payroll/', views.PayrollView.as_view(), name="add-payroll"),
    path('payroll/new/', views.SelectCompanyView.as_view(), name="select-company"),
    path('payroll/new/<int:pk>/', views.PayrollCreateView.as_view(), name="create-payroll"),
    path('pdf/<slug:pay>/', views.myview, name="pdf"),
    path('payslip/<slug:pay>/', views.payslip, name="payslip"),
    # path('updatepayroll/<int:pk>/', views.payrollUpdate, name="updatepayroll"),
    
]


#  path('purchases/', views.PurchaseView.as_view(), name='purchases-list'), 
#     path('purchases/new', views.SelectSupplierView.as_view(), name='select-supplier'), 
#     path('purchases/new/<pk>', views.PurchaseCreateView.as_view(), name='new-purchase'),    
#     path('purchases/<pk>/delete', views.PurchaseDeleteView.as_view(), name='delete-purchase'),

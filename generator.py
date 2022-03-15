import random
from datetime import datetime
import string

time = datetime.today().strftime("%Y")

def emp_id():
    number= random.randint(0,9999)
    return f"EMP-{number}-{time}"

def get_nin():
    nin_num = random.randint(0,9999999999)
    return f"NG-{nin_num}" 

def get_bank_account():
    tin = random.randint(0,9999999999)
    return tin

str="1234123412341234"
def masking(number, start_num=0, end_num=0, char="#"):
  number_len = len(number)
  mask_len = number_len - abs(start_num) - abs(end_num)
  return(number[:abs(start_num)] + (char * mask_len) + number[-end_num:])

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))



# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib import messages
# from django.utils.http import urlsafe_base64_encode
# from django.utils.encoding import force_bytes

# from payroll.models import Department, Grade, Payroll, Employee, Tax

# from payroll.forms import PayrollForm, EmployeeForm

# def home(request):
#     return render(request,"home.html")
    

# def addEmployee(request):
#     form = EmployeeForm(request.POST or None, request.FILES or None)

#     if form.is_valid():
#         employee = form.save()
#         employee.save()

#         messages.success(request, "Employee has been created successfully")
#         return redirect('employeedashboard')
#     context = {
#         "form": form
#     }
#     return render(request, 'addEmployee.html', context)

# def addPayroll(request):
#     form = PayrollForm(request.POST or None, request.FILES or None)

#     if form.is_valid():
#         pay = form.save()
#         pay.save()

#         messages.success(request, "Payroll has been created successfully")
#         return redirect('payrolldashboard')
#     context = {
#         "form": form
#     }
#     return render(request,"addpayroll.html", context)

# def employeedashboard(request):
#     employee = Employee.objects.all()
#     context = {
#         "employee": employee,
        
#     }
#     return render(request,"emp_dashboard.html", context)

# def payrolldashboard(request):
#     payroll = Payroll.objects.all()
#     context = {
#         "payroll": payroll
#     }
#     return render(request,"pay_dashboard.html", context)

# def updatepayroll(request, pk):

#     payroll = get_object_or_404(Payroll, pk=pk)
#     form = PayrollForm(request.POST or None,request.FILES or None,instance = payroll)
#     if form.is_valid():
#         payroll = form.save(commit=False)
        
#         payroll.author = request.user
#         payroll.save()

#         messages.success(request,"Employee has been Updated")
#         return redirect("payrolldashboard")
#     return render(request,"pay_update.html",{"form":form})

# def deletepayroll(request, pk):
#     pay = get_object_or_404(Payroll, pk=pk)
#     pay.delete()
#     messages.success(request,"Payroll Deleted Successfully")

#     return redirect("payrolldashboard")


# def updateemployee(request, pk):

#     employee = get_object_or_404(Employee, pk=pk)
#     form = EmployeeForm(request.POST or None,request.FILES or None,instance = employee)
#     if form.is_valid():
#         employee = form.save(commit=False)
        
#         employee.author = request.user
#         employee.save()

#         context = {
#             "employee": employee,
#             "uid": urlsafe_base64_encode(force_bytes(employee.id)),
#             "form":form,
#         }

#         messages.success(request,"Employee has been Updated")
#         return redirect("employeedashboard")
#     return render(request,"emp_update.html",context)


# def deleteemployee(request, pk):
#     emp = get_object_or_404(Employee, pk=pk)
#     emp.delete()
#     messages.success(request,"Employee Deleted Successfully")

#     return redirect("emmployeedashboard")


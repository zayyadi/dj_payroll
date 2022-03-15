from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.template.loader import get_template
from django.contrib.auth import login

from xhtml2pdf import pisa

from payroll.process import link_callback
from payroll.models import Grade,Employee,User, DeductionsAndEarnings
from payroll.forms import DepartmentForm, GradeForm, PayrollForm, EmployeeForm, EandDForms, UserCreateForm
from generator import id_generator





def home(request):
    employee = Employee.objects.all()


    return render(request,"home.html", {"employee": employee})

@user_passes_test(lambda u: u.is_superuser)
def dashboard(request):
    employee = Employee.objects.all()
    variable = DeductionsAndEarnings.objects.all()

    context = {
        
        "employee": employee,
        "variable": variable
    }
    return render(request, "emp_dashboard.html", context)

@user_passes_test(lambda u: u.is_superuser)
def addDepartment(request):
    form = DepartmentForm(request.POST or None,request.FILES or None)

    if form.is_valid():
        article = form.save()
        article.save()
        messages.success(request,"Department created successfully")
        return redirect('dashboard')
    context = {
        "form": form,
    }

    
    return render(request, "addDept.html", context)

@user_passes_test(lambda u: u.is_superuser)
def addGrade(request):
    form = GradeForm(request.POST or None,request.FILES or None)

    if form.is_valid():
        article = form.save()
        article.save()

        messages.success(request,"Grade created successfully")
        return redirect('dashboard')
    context = {
        "form": form,
    }
    
    return render(request, "addGrade.html", context)

@user_passes_test(lambda u: u.is_superuser)
def addPayroll(request):
    form = PayrollForm(request.POST or None,request.FILES or None)

    if form.is_valid():
        article = form.save()
        article.save()

        messages.success(request,"Payroll created successfully")
        return redirect('dashboard')
    context = {
        "form": form,
    }
    return render(request, "addpayroll.html", context)

@user_passes_test(lambda u: u.is_superuser)
def addEandD(request):
    form = EandDForms(request.POST or None,request.FILES or None)

    if form.is_valid():
        article = form.save()
        article.save()

        messages.success(request,"Employee Earnings created successfully")
        return redirect('dashboard')
    context = {
        "form": form,
    }
    return render(request, "addEandD.html", context)

@user_passes_test(lambda u: u.is_superuser)
def payslip(request,pk):
    employee = get_object_or_404(DeductionsAndEarnings, pk=pk)
    context = {
        "employee": employee,
    }

    return render(request, "payslip_template.html", context)

@user_passes_test(lambda u: u.is_superuser)
def payrollUpdate(request, pk):
    employee = get_object_or_404(DeductionsAndEarnings, pk=pk)
    form = EandDForms(request.POST or None, request.FILES or None,instance = employee)
    if form.is_valid():
        emp = form.save(commit=False)
        
        emp.author = request.user
        emp.save()

        messages.success(request,"Payroll has been Updated")
        return redirect("dashboard")
    return render(request,"pay_update.html",{"form":form})

def myview(request, pk):
    template_path = 'payslip_temp.html'
    var = get_object_or_404(DeductionsAndEarnings, pk=pk)
    context = {'var': var}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response, link_callback=link_callback)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def SignUp(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            first_name = user.first_name
            last_name = user.last_name
            name = first_name + ' ' + last_name
            Employee.objects.create(name=name, user=user)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreateForm()
    return render(request, 'account/signup.html', {'form': form})

def CreateUserProfile(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            # try:
            password = User.objects.make_random_password()
            username = profile.name.split()[0] + id_generator()
            user = User.objects.create(username=username, user_type="P")
            user.set_password(password)
            user.save_base(raw=True)
            profile.user = user
            profile.save()
            return redirect('dashboard')
    else:
        form = EmployeeForm()
    return render(request, 'user_profile/profile_create.html', {'form': form})
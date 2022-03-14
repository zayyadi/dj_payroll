from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib import messages
from django.views.generic import View
from django.template.loader import render_to_string
from django.contrib.auth.decorators import user_passes_test
from django.template.loader import get_template
from xhtml2pdf import pisa

from django_xhtml2pdf.utils import generate_pdf

from payroll.process import link_callback

from payroll.models import Grade,Employee,Payroll, DeductionsAndEarnings
from payroll.forms import DepartmentForm, GradeForm, PayrollForm, EmployeeForm, EandDForms





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
def employeeUpdate(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    form = EmployeeForm(request.POST or None, request.FILES or None,instance = employee)
    if form.is_valid():
        emp = form.save(commit=False)
        
        emp.author = request.user
        emp.save()

        messages.success(request,"Employee has been Updated")
        return redirect("dashboard")
    return render(request,"emp_update.html",{"form":form})

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



# class GeneratePdf(View):
#      def get(self, request, *args, **kwargs):
#         data = DeductionsAndEarnings.objects.get(id=1)
#         open('templates/payslip_temp.html', "w").write(render_to_string('payslip_tem.html', {'data': data}))

#         # Converting the HTML template into a PDF file
#         pdf = html_to_pdf('payslip_temp.html')
         
#          # rendering the template
#         return HttpResponse(pdf, content_type='application/pdf')

# def myview(response, pk):
#     
#     open('templates/payslip_temp.html', "w").write(render_to_string('payslip_tem.html', {'data': data}))
#     resp = HttpResponse(content_type='application/pdf')
#     result = generate_pdf('payslip_template.html', file_object=resp)
#     return result

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
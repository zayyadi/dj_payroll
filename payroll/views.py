from django.shortcuts import render, redirect, get_object_or_404, HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.template.loader import get_template
from django.db.models.functions import TruncMonth
from django.db.models import Sum
from django.views.generic import ListView
from django.views.generic.edit import CreateView

from django.forms import inlineformset_factory


from xhtml2pdf import pisa

from payroll.process import link_callback
from payroll.models import (
    Grade,
    Employee,
    Company,
    Payroll
)
from payroll.forms import (
    DepartmentForm,
    GradeForm,
    EmployeeForm,
    MonthForm

)


def home(request):
    employees = Employee.objects.all()
    employees_count = employees.count()


    payee_count = Payroll.objects.order_by('month_year').distinct('month_year').count()

    nhif_count = Payroll.objects.order_by('month_year').distinct('month_year').count()

    nssf_count = Payroll.objects.order_by('month_year').distinct('month_year').count()

    bank_report_count = Payroll.objects.order_by('month_year').distinct('month_year').count()

    return render(request, 'payroll/index.html',
                  {'employees_count': employees_count, 'nhif_count': nhif_count,
                   'bank_report_count': bank_report_count, 'kra_count': payee_count, 'nssf_count':nssf_count})

def employees(request):
    employees = Employee.objects.all()
    if request.method == 'POST':
        form = EmployeeForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Employee added successfully")
        else:
            messages.error(request, "Error adding employee")
    else:
        form = EmployeeForm()
    return render(request, 'payroll/employees.html', {'employees': employees, 'employee_form': form})

def kra_view(request):
    months = Payroll.objects.order_by('month_year').distinct('month_year')
    return render(request, 'payroll/kra.html', {'months': months})


def payee_report(request, month_year):
    payroll = Payroll.objects.filter(month_year=month_year)
    gross_pay_total = Payroll.objects.filter(month_year=month_year).aggregate(Sum('employee_id.grade.gross_pay'))['employee_id.grade.gross_pay__sum']
    cooperatve_contribution_total = Payroll.objects.filter(month_year=month_year).aggregate(Sum('cooperative_deduction'))
    staff_loan_total = Payroll.objects.filter(month_year=month_year).aggregate(Sum('staff_loan_deduction'))
    staff_pension_total = Payroll.objects.filter(month_year=month_year).aggregate(Sum('pension_emp'))
    tax_chargable = Payroll.objects.filter(month_year=month_year).aggregate(Sum('taxable_income'))['taxable_income__sum']
    consolidated_relief = Payroll.objects.filter(month_year=month_year).aggregate(Sum('consolidated_relief'))
    total_tax = Payroll.objects.filter(month_year=month_year).aggregate(Sum('payee'))['payee__sum']
    return render(request, 'payroll/kra_report.html', {'payroll': payroll, 'monthyear': month_year,
                                                       'gross_pay_total': gross_pay_total,
                                                       'nssf_deduction': cooperatve_contribution_total['nssf_deduction__sum'],
                                                       'nssf_deduction': staff_loan_total['staff_loan_deduction__sum'],
                                                       'pension': staff_pension_total['pension_emp__sum'],
                                                       'tax_chargable': tax_chargable,
                                                       'personal_relief': consolidated_relief['consolidated_relief__sum'],
                                                       'total_tax': total_tax})


# def dashboard(request):
#     employee = Employee.objects.all()
#     variable = Payroll.objects.all()
#     total_pay = BasePayroll.objects.annotate(month=TruncMonth('start_date')).values('month').annotate(total_amount=Sum('deduction_earning__employee__payroll__grade__gross_pay'))

#     context = {
#         "total":total_pay,
#         "employee": employee,
#         "variable": variable
#     }
#     return render(request, "emp_dashboard.html", context)

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

class CreateEmployee(CreateView):
    template_name = "addEmployee.html"
    form_class = EmployeeForm
    success_url = '/'

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

def generate_payroll(request, employee_id):
    if request.method == 'POST':
        form = MonthForm(request.POST)

        if form.is_valid():
            employee = Employee.objects.get(pk=employee_id)
            # calculate_payroll = EmployeePayroll(int(employee.basic_salary))
            payroll = Payroll.objects.create(employee_id_id=employee_id)
            payroll.month_year = form.cleaned_data['month']
            payroll.save()
            return HttpResponseRedirect('/')
    else:
        form = MonthForm()

    payroll = Payroll.objects.filter(employee_id_id=employee_id)

    return render(request, 'payroll/calculate_payroll_employee.html', {'form': form, 'payrolls': payroll})


class PayrollView(ListView):
    model = Payroll
    template_name = "payroll_list.html"
    context_object_name = 'employee'
    ordering = ['-slug']
    paginate_by = 10

@user_passes_test(lambda u: u.is_superuser)
def payslip(request,pay):
    employee = get_object_or_404(DeductionsAndEarnings, slug=pay)
    company = Company.objects.all()
    context = {
        "employee": employee,
        "company" : company,
    }

    return render(request, "payslip_template.html", context)


def myview(request, pay):
    template_path = 'payslip_temp.html'
    var = get_object_or_404(DeductionsAndEarnings, slug=pay)
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



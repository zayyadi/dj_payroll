from django import forms
from django.forms import formset_factory, ModelForm
from .models import BasePayroll, Company, DeductionsAndEarnings, Payroll, Employee,Department, Grade, Unit
from django.contrib.auth import get_user_model
# from django.contrib.auth.forms import UserCreationForm

from crispy_forms.helper import FormHelper
from date.forms import MonthField

from crispy_forms.layout import Field, Layout, Div, ButtonHolder, Submit

class CompanyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['company_name'].widget.attrs.update({'class': 'textinput form-control', 'pattern' : '[a-zA-Z\s]{1,50}', 'title' : 'Alphabets and Spaces only'})
        self.fields['phone'].widget.attrs.update({'class': 'textinput form-control', 'maxlength': '10', 'pattern' : '[0-9]{10}', 'title' : 'Numbers only'})
        self.fields['contact_person'].widget.attrs.update({'class': 'textinput form-control', 'pattern' : '[a-zA-Z\s]{1,50}', 'title' : 'Alphabets and Spaces only'})
        self.fields['address'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['email'].widget.attrs.update({'class': 'textinput form-control'})
    class Meta:
        models = Company
        fields = (
            'company_name',
            'phone',
            'contact_person',
            'address',
            'email',
        )

class BasePayrollForm(forms.ModelForm):
    class Meta:
        models = BasePayroll
        fields = '__all__'

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ('name','gross_pay')

class PayrollForm(forms.ModelForm):
    class Meta:
        model = Payroll
        fields = (
            "grade",
            "taxable",
        )

        #blank label, removes the label
        labels = {
            "grade": "grade of employee salary scale",
            "taxable": "taxable employee salary"
        }
        #we are using widgets and attrs to update the placeholder
        widgets = {
            "grade": forms.Select(),
            "taxable": forms.CheckboxInput(),
        }

class EmployeeForm(ModelForm):
    date_of_birth = forms.DateField(widget=forms.TextInput(attrs={'class': 'datepicker'}))
    date_of_employment = forms.DateField(widget=forms.TextInput(attrs={'class': 'datepicker'}))

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Div(Field('first_name'), css_class='col-md-4', ),
                Div(Field('last_name'), css_class='col-md-4', ),
                Div(Field('middle_name'), css_class='col-md-4', ),
                Div(Field('gender'), css_class='col-md-4', ),
                Div(Field('date_of_birth'), css_class='col-md-4', ),
                Div(Field('residential_status'), css_class='col-md-4', ),
                # Div(Field('nin'), css_class='col-md-4', ),
                Div(Field('allowances'), css_class='col-md-4', ),
                css_class='row',
            ),
            Div(
                Div(Field('nin_no'), css_class='col-md-4', ),
                Div(Field('tin_no'), css_class='col-md-4', ),
                Div(Field('department'), css_class='col-md-4', ),
                Div(Field('unit'), css_class='col-md-4', ),
                Div(Field('payroll'), css_class='col-md-4', ),
                Div(Field('bank'), css_class='col-md-4', ),
                Div(Field('bank_account_name'), css_class='col-md-4', ),
                Div(Field('bank_account_number'), css_class='col-md-4', ),
                css_class='row',
            ),
            Div(
                Div(Field('bank_branch'), css_class='col-md-4', ),
                Div(Field('employee_personal_number'), css_class='col-md-4', ),
                Div(Field('date_of_employment'), css_class='col-md-4', ),
                Div(Field('contract_type'), css_class='col-md-4', ),
                Div(Field('job_title'), css_class='col-md-4', ),
                Div(Field('email'), css_class='col-md-4', ),
                Div(Field('phone'), css_class='col-md-4', ),
                css_class='row',
            ),
            ButtonHolder(
                Submit('submit', 'Save', css_class='button white')
            )
        )
        super(EmployeeForm, self).__init__(*args, **kwargs)

class MonthForm(forms.Form):
    month = MonthField()


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = "__all__"
class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = "__all__"


class EmployeeSearchForm(forms.Form):
    q = forms.CharField()
    c = forms.ModelChoiceField(
        queryset=Employee.objects.all().order_by('first_name'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['c'].label = ''
        self.fields['c'].required = False
        self.fields['c'].label = 'Employee'
        self.fields['q'].label = 'Search For'
        self.fields['q'].widget.attrs.update(
            {'class': 'form-control'})


# class EandDForms(forms.ModelForm):
# #     class Meta:
# #         model = DeductionsAndEarnings
# #         fields = (
# #             'employee',
# #             'lateness_deduction',
# #             'damage_deduction',
# #             'absence_deduction',
# #             'activate_overtime_allowance',
# #             'activate_leave_allowance',
# #             'activate_cooperative_deduction',
# #             'activate_staff_loan_deduction',
# #             'late_hours',
# #             'overtime_hours',
# #             'days_absent',
# #             'lateness_amount_deduction_rate',
# #             'absence_amount_deduction_rate',
# #             'cooperative_deduction_rate',
# #             'staff_loan_deduction_rate',
# #             'overtime',
# #             'water_fee',
# #             'development_fee'

# #         )

# #         widget = {
# #             "employee": forms.Select(),
# #             "lateness_deduction": forms.CheckboxInput(),
# #             "damage_deduction": forms.CheckboxInput(),
# #             "absence_deduction": forms.CheckboxInput(),
# #             "activate_overtime_allowance": forms.CheckboxInput(),
# #             "activate_leave_allowance": forms.CheckboxInput(),
# #             "hours": forms.NumberInput(),
# #             "rate": forms.NumberInput(),
from random import choices
from django import forms
from .models import DeductionsAndEarnings, Payroll, Employee,Department, Grade


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

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = (
            "department",
            "first_name",
            "last_name",
            "email",
            "gender",
            "address",
            "payroll",
        )

        label = {
            "department": "employee Department",
            "first_name": "employee First Name",
            "last_name": "employee Last Name",
            "email": "employee Email",
            "gender": "employee Gender",
            "address": "employee Address",
            "payroll": "employee payroll class"
        }

        widget = {
            "department": forms.Select(),
            "first_name": forms.TextInput(),
            "last_name": forms.TextInput(),
            "email": forms.EmailField(),
            "gender": forms.ChoiceField(),
            "address": forms.TextInput(),
            "payroll": forms.NumberInput(),
        }

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ('name',)

class EandDForms(forms.ModelForm):
    class Meta:
        model = DeductionsAndEarnings
        fields = (
            'employee',
            'lateness_deduction',
            'damage_deduction',
            'absence_deduction',
            'activate_overtime_allowance',
            'activate_leave_allowance',
            'hours',
            'rate',
        )

        widget = {
            "employee": forms.Select(),
            "lateness_deduction": forms.CheckboxInput(),
            "damage_deduction": forms.CheckboxInput(),
            "absence_deduction": forms.CheckboxInput(),
            "activate_overtime_allowance": forms.CheckboxInput(),
            "activate_leave_allowance": forms.CheckboxInput(),
            "hours": forms.NumberInput(),
            "rate": forms.NumberInput(),
        }

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
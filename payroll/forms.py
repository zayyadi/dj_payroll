from random import choices
from django import forms
from .models import DeductionsAndEarnings, Payroll, Employee,Department, Grade
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


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

class SelectEmployeeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['employee'].queryset = Employee.objects.filter(is_active=False)
        self.fields['employee'].widget.attrs.update({'class': 'textinput form-control'})
    class Meta:
        model = Employee
        fields = ['employee']


class EmployeeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class': 'textinput form-control', 'pattern' : '[a-zA-Z\s]{1,50}', 'title' : 'Alphabets and Spaces only'})
        self.fields['last_name'].widget.attrs.update({'class': 'textinput form-control', 'pattern' : '[a-zA-Z\s]{1,50}', 'title' : 'Alphabets and Spaces only'})
        self.fields['phone'].widget.attrs.update({'class': 'textinput form-control', 'maxlength': '10', 'pattern' : '[0-9]{10}', 'title' : 'Numbers only'})
        self.fields['email'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['address'].widget.attrs.update({'class': 'textinput form-control'})
    class Meta:
        model = Employee
        fields = (
            "department",
            "first_name",
            "last_name",
            "phone",
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
            'activate_cooperative_deduction',
            'activate_staff_loan_deduction',
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

USER_CHOICES = [
    ('A', 'Admin'),
    ('E', 'Employee')
]

class UserCreateForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=USER_CHOICES, required=True, widget=forms.RadioSelect)
    class Meta:
        fields = ("first_name", "last_name", "username", "email", "password1", "password2", "user_type")
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Username"
        self.fields["email"].label = "Email address"
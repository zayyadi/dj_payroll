from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, AbstractUser

from decimal import Decimal

from generator import emp_id, get_nin, get_bank_account, masking
from num2words import num2words

GENDER=(
    ('others', 'Others'),
    ('male', 'Male'),
    ('female', 'Female'),
)

DESIGNATION = (
    ('casual', 'Casual'),
    ('floor', 'Floor Worker'),
    ('packer', 'packer'),
    ('label', 'Label Operator'),
    ('supervisor', 'SUpervisor'),
    ('manager', 'Manager'),
    ('C.O.O', 'C.O.O'),
)

USER_CHOICES = [
    ('A', 'Admin'),
    ('E', 'Employee')
]

class User(AbstractUser):
    user_type = models.CharField(choices=USER_CHOICES, max_length=2)

    def is_admin(self):
        if self.user_type == 'D':
            return True
        else:
            return False

    def is_employee(self):
        if self.user_type == 'P':
            return True
        else:
            return False

    class Meta:
        ordering = ('id',)


class Department(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True, blank=False)

    def __str__(self):
        return self.name


class Grade(models.Model):
    name = models.CharField(max_length=255,blank=True, unique=True)
    gross_pay = models.DecimalField(max_digits=12, decimal_places=5, blank=False)
    annual_gross_pay = models.DecimalField(max_digits=12, decimal_places=5, blank=True)

    def __str__(self):
        return self.name

    @property
    def get_annual_gross_pay(self):
        return self.gross_pay*12

    def save(self,*args, **kwargs):
        self.annual_gross_pay= self.get_annual_gross_pay

        super(Grade, self).save(*args, **kwargs)

class Payroll(models.Model):
    grade = models.ForeignKey(Grade, on_delete=models.PROTECT, related_name='payroll_grade')
    housing = models.DecimalField(max_digits=12, decimal_places=5, blank=True)
    transport = models.DecimalField(max_digits=12, decimal_places=5, blank=True)
    basic = models.DecimalField(max_digits=12, decimal_places=5, blank=True)
    taxable = models.BooleanField(default=False)
    pension_emp = models.DecimalField(max_digits=12, decimal_places=5, blank=True)
    pension_emly = models.DecimalField(max_digits=12, decimal_places=5, blank=True)
    pension = models.DecimalField(max_digits=12, decimal_places=5, blank=True)
    gross_income = models.DecimalField(max_digits=12, decimal_places=5, blank=True)
    consolidated_relief = models.DecimalField(max_digits=12, decimal_places=5, blank=True)
    taxable_income = models.DecimalField(max_digits=12, decimal_places=5, blank=True)
    payee = models.DecimalField(max_digits=12, decimal_places=5, blank=True)
    

    def __str__(self):
        return str(self.grade)
    
    @property
    def get_basic(self):
        return self.grade.gross_pay * 40 / 100
    
    @property
    def get_housing(self):
        return self.grade.gross_pay * 10 / 100

    @property
    def get_transport(self):
        return self.grade.gross_pay * 10 / 100
    
    @property
    def get_bht(self):
        return self.get_basic + self.housing +self.get_transport
    
    @property
    def get_employee_pension(self):
        if self.grade.annual_gross_pay <= 360000:
            return 0
        return self.get_bht * 8/100

    @property
    def get_employer_pension(self):
        if self.grade.annual_gross_pay <= 360000:
            return 0
        return self.get_bht * 10/100
    
    @property
    def add_pension(self):
        return self.get_employee_pension + self.get_employer_pension

    @property
    def pension_logic(self):
        if self.grade.annual_gross_pay <= 360000:
            return self.add_pension==0
        return self.get_employee_pension

    @property
    def twenty_percents(self):
        return self.grade.annual_gross_pay * 20 / 100

    @property
    def calc_cons(self):
        return self.grade.annual_gross_pay * 1/100 + self.twenty_percents

    @property
    def calc_conss(self):
        return 200000 + self.grade.annual_gross_pay * 20/100

    def get_consolidated_relief(self):
        
        if self.calc_cons > self.calc_conss:
            return self.calc_cons
        return self.calc_conss
        

    @property
    def get_taxable_income(self) -> Decimal:
        return self.grade.annual_gross_pay - self.consolidated_relief

    @property
    def first_taxable(self):
        if self.get_taxable_income <= 88000:
            return 0
    
    @property
    def second_taxable(self):
        if self.get_taxable_income - 300000<= 300000:
            return(300000 * 7/100)
    
    @property        
    def third_taxable(self):
        if self.get_taxable_income - 600000 >= 300000:
            return(300000 * 11/100)
    
    @property        
    def fourth_taxable(self):
        if self.get_taxable_income - 1100000 >= 500000:
            return(500000 * 15/100)
    
    @property
    def fifth_taxable(self):    
        if self.get_taxable_income - 1600000 >= 500000:
            return(500000 * 19/100)
            
    @property        
    def payee_logic(self):
        if self.get_taxable_income <= 88000:
            return self.first_taxable
        elif self.get_taxable_income <= 300000:
            return self.second_taxable
        elif self.get_taxable_income > 300000:
            return self.second_taxable + self.third_taxable
        elif self.get_taxable_income >600000:
            return self.second_taxable + self.third_taxable + self.fourth_taxable
        elif self.get_taxable_income >1100000:
            return self.second_taxable + self.third_taxable + self.fourth_taxable + self.fifth_taxable


    def save(self, *args, **kwargs):
        self.basic = self.get_basic
        self.housing = self.get_housing
        self.transport = self.get_transport
        self.pension_emp = self.get_employee_pension
        self.pension_emly = self.get_employer_pension
        self.pension = self.pension_logic
        self.gross_income = self.grade.gross_pay - self.pension_logic
        self.consolidated_relief = self.get_consolidated_relief()
        self.taxable_income = self.get_taxable_income
        self.payee = self.payee_logic

        if self.basic >= 30000:
            self.taxable = True

        super(Payroll, self).save(*args, **kwargs)

class Bank(models.Model):
    name = models.CharField(max_length=255, default="Zenith Bank", blank=False)

    def __str__(self):
        return self.name



class Employee(models.Model):
    id = models.AutoField(primary_key=True, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_profile')
    Employee_id = models.CharField(default=emp_id,max_length=255,editable=False)
    nin = models.CharField(default=get_nin, max_length=255, editable=False)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name="department")
    payroll = models.ForeignKey(Payroll, on_delete=models.PROTECT, blank=True, related_name='employee_pay')
    first_name = models.CharField(max_length=255, blank=False, verbose_name='first name')
    last_name = models.CharField(max_length=255, blank=False, verbose_name='last   name')
    email = models.CharField(max_length=255, blank=True, verbose_name='email', unique=True)
    gender = models.CharField(max_length=255, choices=GENDER, default='others', blank=False, verbose_name='gender')
    address = models.CharField(max_length=255, blank=False, unique=True, verbose_name='address')
    created = models.DateTimeField(default=timezone.now, blank=False)
    net_pay = models.DecimalField(max_digits=12, decimal_places=5, default=0.0, blank=True)
    designation = models.CharField(max_length=255, choices=DESIGNATION, default='casual', blank=False, verbose_name='designation')
    
    bank = models.ForeignKey(Bank, on_delete=models.PROTECT, related_name="employee_bank")
    bank_account = models.CharField(default=get_bank_account, max_length=255, editable=False)
    
    @property
    def get_email(self):
        return self.first_name + "." + self.last_name + "@polarpetrochemicalsltd.com"

    @property
    def get_net_pay(self):
        return self.payroll.gross_income - (self.payroll.payee / 12)
    @property
    def get_masked_acc(self):
        return masking(self.bank_account, 0, 4, "*")
    
    class Meta:
        ordering = ['-created']

    def save(self,*args, **kwargs):
        self.email= self.get_email
        self.net_pay = self.get_net_pay

        super(Employee, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} - {self.last_name}"


class DeductionsAndEarnings(models.Model):
    employee = models.ForeignKey(
        Employee, 
        on_delete=models.PROTECT, 
        related_name='employees_deduction'
    )
    lateness_deduction = models.BooleanField(default=False)
    damage_deduction = models.BooleanField(default=False)
    absence_deduction = models.BooleanField(default=False)
    activate_overtime_allowance = models.BooleanField(default=False)
    activate_leave_allowance = models.BooleanField(default=False)
    overtime = models.DecimalField(
        max_digits=12,
        decimal_places=5,
        blank=True,
        verbose_name = "Overtime worked Allowance"
    )
    leave_allowance = models.DecimalField(
        max_digits=12, 
        decimal_places=5, 
        blank=True,
        verbose_name="Annual leave Allowance"
    )
    lateness = models.DecimalField(
        max_digits=12, 
        decimal_places=5, 
        blank=True,
        verbose_name="late to work deduction"
    )
    absence = models.DecimalField(
        max_digits=12, 
        decimal_places=5, 
        blank=True,
        verbose_name="absence from work deductions"
    )
    damage = models.DecimalField(
        max_digits=12, 
        decimal_places=5, 
        blank=True, 
        verbose_name="equipment damages deductions [Optional]"
    )
    hours = models.IntegerField(default=0)
    rate = models.DecimalField(
        max_digits=12, 
        decimal_places=5, 
        default=300, 
        blank=True
    )
    total_dedcutions = models.DecimalField(
        max_digits=12,
        default=0.0, 
        decimal_places=5, 
        blank=True
    )
    total_allowances = models.DecimalField(
        max_digits=12,
        default=0.0, 
        decimal_places=5, 
        blank=True
    )
    num2word= models.CharField(
        max_length=255,
        blank=True, 
        editable=False)
    net_pay_after_ed = models.DecimalField(
        max_digits=12,
        default=0.0, 
        decimal_places=5, 
        blank=True,
        verbose_name="net pay fater Earnings and Deductions"
    )

    # start_date = models.DateField()
    # end_date = models.DateField()

    class Meta:
        verbose_name_plural="Earnings & Deductions"
    
    @property
    def get_annual_leave(self):
        if self.activate_leave_allowance is True:
            return self.employee.payroll.grade.annual_gross_pay * 10 / 100
        return 0

    @property
    def get_overtime(self):
        if self.activate_overtime_allowance is True:
            return self.rate * self.hours
        return 0

    @property
    def get_lateness(self):
        if self.lateness_deduction is True:
            return self.rate * self.hours
        return 0
    
    @property
    def get_absence(self):
        if self.absence_deduction is True:
            return self.rate * self.hours
        return 0
    
    @property
    def get_damage(self):
        if self.damage_deduction is True:
            return self.employee.net_pay * 10 / 100
        return 0 

    @property
    def get_total_deduction(self):
        return self.get_damage + self.get_absence + self.get_lateness

    @property
    def get_total_allowances(self):
        return self.get_overtime + self.get_annual_leave

    @property
    def get_netpay_after_deduction_earning(self):
        return self.employee.net_pay + self.total_allowances- self.total_dedcutions

    @property
    def get_num2words(self):
        return num2words(self.get_netpay_after_deduction_earning)

    def save(self,*args, **kwargs):
        self.leave_allowance = self.get_annual_leave
        self.overtime = self.get_overtime
        self.absence = self.get_absence
        self.lateness = self.get_lateness
        self.damage = self.get_damage
        self.total_allowances = self.get_total_allowances
        self.total_dedcutions = self.get_total_deduction
        self.num2word= self.get_num2words
        self.net_pay_after_ed= self.get_netpay_after_deduction_earning
        super(DeductionsAndEarnings, self).save(*args, **kwargs)

    def __str__(self):
        return F"your {self.leave_allowance}    {self.overtime}     {self.lateness} {self.absence}"



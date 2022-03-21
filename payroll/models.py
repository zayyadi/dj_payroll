from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, AbstractUser
from django.core.validators import RegexValidator
from django.urls import reverse

from decimal import Decimal

from generator import emp_id, get_nin, get_bank_account
from payroll.choices import *
from payroll.logic import *


class Company(models.Model):
    company_name = models.CharField(max_length=150)
    phone = models.BigIntegerField()
    contact_person = models.CharField(max_length=100)
    address = models.CharField(max_length=150)
    email = models.CharField(max_length=100)
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Companies"

    def __str__(self):
        return self.company_name


class Base_payroll(models.Model):
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="company_payroll"
    )
    start_date = models.DateField()
    end_date = models.DateField()
    payment_method = models.CharField(max_length=3, choices=PAYMENT_METHOD, default="B")


class Department(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True, blank=False)

    def __str__(self):
        return self.name


class Grade(models.Model):
    name = models.CharField(max_length=255, blank=True, unique=True)
    gross_pay = models.DecimalField(max_digits=12, decimal_places=5, blank=False)
    annual_gross_pay = models.DecimalField(max_digits=12, decimal_places=5, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.annual_gross_pay = get_annual_gross_pay(self)

        super(Grade, self).save(*args, **kwargs)


class Payroll(models.Model):
    grade = models.ForeignKey(
        Grade, on_delete=models.PROTECT, related_name="payroll_grade"
    )
    housing = models.DecimalField(max_digits=12, decimal_places=5, blank=True)
    transport = models.DecimalField(max_digits=12, decimal_places=5, blank=True)
    basic = models.DecimalField(max_digits=12, decimal_places=5, blank=True)
    taxable = models.BooleanField(default=False)
    pension_emp = models.DecimalField(
        max_digits=12, decimal_places=5, blank=True, verbose_name="pension Employee"
    )
    pension_emly = models.DecimalField(
        max_digits=12, decimal_places=5, blank=True, verbose_name="pension Employer"
    )
    pension = models.DecimalField(max_digits=12, decimal_places=5, blank=True)
    gross_income = models.DecimalField(max_digits=12, decimal_places=5, blank=True)
    consolidated_relief = models.DecimalField(
        max_digits=12, decimal_places=2, blank=True
    )
    taxable_income = models.DecimalField(max_digits=12, decimal_places=2, blank=True)
    payee = models.DecimalField(max_digits=12, decimal_places=2, blank=True)

    @property
    def calc_cons(self):
        return self.grade.annual_gross_pay * 1 / 100

    @property
    def calc_conss(self):
        return 200000

    @property
    def get_taxable_income(self) -> Decimal:
        return (
            self.grade.annual_gross_pay
            - self.consolidated_relief
            - (self.pension_emp * 12)
        )

    def __str__(self):
        return f"{self.grade}         {self.grade.gross_pay}"

    def save(self, *args, **kwargs):
        self.basic = get_basic(self)
        self.housing = get_housing(self)
        self.transport = get_transport(self)
        self.pension_emp = get_employee_pension(self)
        self.pension_emly = get_employer_pension(self)
        self.pension = pension_logic(self)
        self.gross_income = self.grade.gross_pay - pension_logic(self)
        self.consolidated_relief = calc_consolidated_relief(self)
        self.taxable_income = self.get_taxable_income
        self.payee = payee_logic(self)

        if self.basic >= 30000:
            self.taxable = True

        super(Payroll, self).save(*args, **kwargs)


class Employee(models.Model):
    id = models.AutoField(primary_key=True, unique=True, editable=False)
    Employee_id = models.CharField(default=emp_id, max_length=255, editable=False)
    nin = models.CharField(default=get_nin, max_length=255, editable=False)
    department = models.ForeignKey(
        Department, on_delete=models.PROTECT, related_name="department"
    )
    payroll = models.ForeignKey(
        Payroll, on_delete=models.PROTECT, blank=True, related_name="employee_pay"
    )
    first_name = models.CharField(
        max_length=255, blank=False, verbose_name="first name"
    )
    last_name = models.CharField(max_length=255, blank=False, verbose_name="last name")
    full_name = models.SlugField(
        max_length=255, blank=True, unique=True, verbose_name="full name"
    )
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
    )
    phone = models.CharField(
        validators=[phone_regex], default=1234567890, max_length=17, blank=True
    )
    email = models.CharField(
        max_length=255, blank=True, verbose_name="email", unique=True
    )
    gender = models.CharField(
        max_length=255,
        choices=GENDER,
        default="others",
        blank=False,
        verbose_name="gender",
    )
    address = models.CharField(
        max_length=255, blank=False, unique=True, verbose_name="address"
    )
    created = models.DateTimeField(default=timezone.now, blank=False)
    net_pay = models.DecimalField(
        max_digits=12, decimal_places=2, default=0.0, blank=True
    )
    designation = models.CharField(
        max_length=255,
        choices=DESIGNATION,
        default="casual",
        blank=False,
        verbose_name="designation",
    )
    bank = models.CharField(
        max_length=5, choices=BANK, default="Z", verbose_name="employee BANK"
    )
    bank_account = models.CharField(
        default=get_bank_account, max_length=255, editable=False
    )
    is_active = models.BooleanField(default=True)

    def get_masked_acc(self):
        return masking(self.bank_account, 0, 4, "*")

    class Meta:
        ordering = ["-created"]

    def get_absolute_url(self):
        return reverse("employee", args=[self.full_name])

    def save(self, *args, **kwargs):
        self.email = self.get_email
        self.net_pay = get_net_pay(self)
        self.full_name = get_slug(self)
        super(Employee, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} - {self.last_name}"


class DeductionsAndEarnings(models.Model):
    base_payroll = models.ForeignKey(
        Base_payroll, on_delete=models.PROTECT, related_name="base_payrolls"
    )
    employee = models.ForeignKey(
        Employee, on_delete=models.PROTECT, related_name="employees_deduction"
    )
    lateness_deduction = models.BooleanField(default=False)
    damage_deduction = models.BooleanField(default=False)
    absence_deduction = models.BooleanField(default=False)
    activate_overtime_allowance = models.BooleanField(default=False)
    activate_leave_allowance = models.BooleanField(default=False)
    activate_cooperative_deduction = models.BooleanField(default=False)
    activate_staff_loan_deduction = models.BooleanField(default=False)
    overtime = models.DecimalField(
        max_digits=12,
        decimal_places=5,
        blank=True,
        verbose_name="Overtime worked Allowance",
    )
    leave_allowance = models.DecimalField(
        max_digits=12,
        decimal_places=5,
        blank=True,
        verbose_name="Annual leave Allowance",
    )
    lateness = models.DecimalField(
        max_digits=12,
        decimal_places=5,
        blank=True,
        verbose_name="late to work deduction",
    )
    absence = models.DecimalField(
        max_digits=12,
        decimal_places=5,
        blank=True,
        verbose_name="absence from work deductions",
    )
    damage = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        verbose_name="equipment damages deductions [Optional]",
    )
    hours = models.IntegerField(default=0)
    days_absent = models.IntegerField(default=0)
    lateness_amount_deduction_rate = models.DecimalField(
        max_digits=12,
        decimal_places=5,
        default=300,
        blank=True,
        verbose_name="lateness amount deduction rate in Naira [Optional]",
    )
    absence_amount_deduction_rate = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=1000,
        blank=True,
        verbose_name="absence amount deduction rate in Naira [Optional]",
    )
    cooperative_deduction_rate = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0,
        blank=True,
        verbose_name="Coperative members amount deduction rate in Naira [Optional]",
    )
    staff_loan_deduction_rate = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0,
        blank=True,
        verbose_name="Staff loan amount deduction rate in Naira [Optional]",
    )
    total_dedcutions = models.DecimalField(
        max_digits=12, default=0.0, decimal_places=5, blank=True
    )
    total_allowances = models.DecimalField(
        max_digits=12, default=0.0, decimal_places=5, blank=True
    )
    water_fee = models.DecimalField(
        max_digits=12, default=150.00, decimal_places=5, blank=True
    )
    development_fee = models.DecimalField(
        max_digits=12, default=200.00, decimal_places=5, blank=True
    )

    num2word = models.CharField(
        max_length=255, blank=True, editable=False
    )
    net_pay_after_ed = models.DecimalField(
        max_digits=12,
        default=0.0,
        decimal_places=2,
        blank=True,
        verbose_name="net pay after Earnings and Deductions",
    )

    class Meta:
        verbose_name_plural = "Earnings & Deductions"

    def save(self, *args, **kwargs):
        self.leave_allowance = get_annual_leave(self)
        self.overtime = get_overtime(self)
        self.absence = get_absence(self)
        self.lateness = get_lateness(self)
        self.damage = get_damage(self)
        self.total_allowances = get_total_allowances(self)
        self.total_dedcutions = get_total_deduction(self)
        self.num2word = get_num2words(self)
        self.net_pay_after_ed = get_netpay_after_deduction_earning(self)
        self.cooperative_deduction_rate = get_cooperative(self)
        self.staff_loan_deduction_rate = get_staff_loan(self)
        super(DeductionsAndEarnings, self).save(*args, **kwargs)

    def __str__(self):
        return f"your {self.leave_allowance}    {self.overtime}     {self.lateness} {self.absence}"

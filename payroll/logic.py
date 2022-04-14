from decimal import Decimal

from generator import masking
from num2words import num2words

from payroll.models import *

# start of grade logic


def get_annual_gross_pay(self):
    return self.gross_pay * 12


# start of payroll logic


def get_basic(self):
    return self.employee_id.grade.gross_pay * 40 / 100


def get_housing(self):
    return self.employee_id.grade.gross_pay * 10 / 100


def get_transport(self):
    return self.employee_id.grade.gross_pay * 10 / 100


def get_bht(self):
    return get_basic(self) + get_housing(self) + get_transport(self)


def get_employee_pension(self):
    if self.employee_id.grade.annual_gross_pay <= 360000:
        return 0
    return get_bht(self) * 8 / 100


def get_employer_pension(self):
    if self.employee_id.grade.annual_gross_pay <= 360000:
        return 0
    return get_bht(self) * 10 / 100


def add_pension(self):
    return get_employee_pension(self) + get_employer_pension(self)


def pension_logic(self):
    if self.employee_id.grade.annual_gross_pay <= 360000:
        return add_pension == 0
    return get_employee_pension(self)


def twenty_percents(self):
    return (self.employee_id.grade.annual_gross_pay) * 20 / 100


def get_consolidated_relief(self):
    if self.calc_cons > self.calc_conss:
        return self.calc_cons
    return self.calc_conss


def calc_consolidated_relief(self):
    return get_consolidated_relief(self) + twenty_percents(self)


def first_taxable(self):
    if self.get_taxable_income <= 88000:
        return 0


def second_taxable(self):
    if self.get_taxable_income < 300000:
        return (self.get_taxable_income) * 7 / 100
    elif self.get_taxable_income >= 300000:
        return 300000 * 7 / 100


def third_taxable(self):
    if (self.get_taxable_income - 300000) < 300000:
        return (self.get_taxable_income - 300000) * 11 / 100
    elif (self.get_taxable_income - 300000) >= 300000:
        return 300000 * 11 / 100

def fourth_taxable(self):
    if (self.get_taxable_income - 600000) >= 500000:
        return 500000 * 15 / 100

    elif (self.get_taxable_income - 600000) <= 500000:
        return (self.get_taxable_income - 600000) * 15 / 100


def fifth_taxable(self):
    if self.get_taxable_income - 1100000 >= 500000:
        return 500000 * 19 / 100
    elif (self.get_taxable_income - 1100000) <= 500000:
        return (self.get_taxable_income - 1100000) * 19 / 100

def sixth_taxable(self):
    if self.get_taxable_income - 1600000 >= 1600000:
        return 1600000 * 21 / 100

    elif (self.get_taxable_income - 1600000) < 1600000:
        return (self.get_taxable_income - 1600000) * 21 / 100

def seventh_taxable(self):
    if self.get_taxable_income - 3200000 > 3200000:
        return 3200000 * 24 / 100
    elif (self.get_taxable_income - 3200000) < 3200000:
        return (self.get_taxable_income - 3200000) * 24 / 100

def payee_logic(self):
    if self.get_taxable_income <= 88000:
        return first_taxable(self)
    elif self.get_taxable_income <= 300000:
        return second_taxable(self)
    elif self.get_taxable_income >= 300000 and self.get_taxable_income < 600000:
        return Decimal(second_taxable(self)) + Decimal(third_taxable(self))
    elif (
        self.get_taxable_income > 300000
        and self.get_taxable_income >= 600000
        and self.get_taxable_income < 1100000
    ):
        return (
            Decimal(second_taxable(self))
            + Decimal(third_taxable(self))
            + Decimal(fourth_taxable(self))
        )
    elif (
        self.get_taxable_income > 300000
        and self.get_taxable_income > 600000
        and self.get_taxable_income >= 1100000
        and self.get_taxable_income < 1600000
        ):
        return (
            Decimal(second_taxable(self))
            + Decimal(third_taxable(self))
            + Decimal(fourth_taxable(self))
            + Decimal(fifth_taxable(self))
        )
    elif (
        self.get_taxable_income > 300000
        and self.get_taxable_income > 600000
        and self.get_taxable_income >= 1100000
        and self.get_taxable_income >= 1600000
        and self.get_taxable_income < 3200000
        ):
           return (
            Decimal(second_taxable(self))
            + Decimal(third_taxable(self))
            + Decimal(fourth_taxable(self))
            + Decimal(fifth_taxable(self))
            + Decimal(sixth_taxable(self))
           )
    elif (
        self.get_taxable_income > 3200000
        ):
        return (
            Decimal(second_taxable(self))
            + Decimal(third_taxable(self))
            + Decimal(fourth_taxable(self))
            + Decimal(fifth_taxable(self))
            + Decimal(sixth_taxable(self))
            + Decimal(seventh_taxable(self))
        )

# start of employee logic


def get_email(self):
    return self.first_name + "." + self.last_name + "@polarpetrochemicalsltd.com"


def get_net_pay(self):
    return self.payroll.gross_income - (self.payroll.payee / 12)


def get_masked_acc(self):
    return masking(self.bank_account, 0, 4, "*")


def get_slug(self):
    return self.first_name + ' ' + self.middle_name + ' ' + self.last_name


# start of E&D logic


def get_annual_leave(self):
    if self.activate_leave_allowance is True:
        return self.employee.payroll.grade.annual_gross_pay * Decimal(0.035)
    return 0


def get_overtime(self):
    if self.activate_overtime_allowance is True:
        return self.overtime * self.overtime_hours
    return 0


def get_lateness(self):
    if self.lateness_deduction is True:
        return self.lateness_amount_deduction_rate * self.late_hours
    return 0


def get_absence(self):
    if self.absence_deduction is True:
        return self.absence_amount_deduction_rate * self.days_absent
    return 0


def get_damage(self):
    if self.damage_deduction is True:
        return self.employee.net_pay * 10 / 100
    return 0



def get_total_deduction(self):
    return (
        get_damage(self)
        + get_absence(self)
        + get_lateness(self)
        + self.water_fee
        + self.development_fee
        + self.cooperative_deduction
        + self.staff_loan_deduction
    )


def get_total_allowances(self):
    return get_overtime(self) + get_annual_leave(self)


def get_netpay_after_deduction_earning(self):
    return self.net_pay + Decimal(self.total_allowances) - Decimal(self.total_deductions)


def get_num2words(self):
    return num2words(get_netpay_after_deduction_earning(self))

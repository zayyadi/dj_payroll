from django.contrib import admin

from payroll.models import Department, Grade, Payroll, Employee, DeductionsAndEarnings, Bank

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('Employee_id', 'bank','department', 'first_name', 'bank_account','net_pay')

class DeductionsAndEarningsAdmin(admin.ModelAdmin):
    list_display = ('employee', 'overtime','leave_allowance','lateness','absence','damage','total_dedcutions', 'total_allowances')


admin.site.register(Department)
admin.site.register(Grade)
admin.site.register(Bank)
admin.site.register(Payroll)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(DeductionsAndEarnings, DeductionsAndEarningsAdmin)



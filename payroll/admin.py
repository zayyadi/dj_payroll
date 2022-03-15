from django.contrib import admin

from payroll.models import Department, Grade, Payroll, Employee, DeductionsAndEarnings, Company, User

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('Employee_id', 'bank','department', 'first_name', 'bank_account','net_pay')

class DeductionsAndEarningsAdmin(admin.ModelAdmin):
    list_display = ('id','employee', 'lateness_deduction', 'absence_deduction', 'activate_overtime_allowance', 'activate_leave_allowance', 'overtime','leave_allowance','lateness','absence','damage','total_dedcutions', 'total_allowances', 'net_pay_after_ed')
    list_display_links = ('employee',)
    list_editable = ('lateness_deduction', 'absence_deduction', 'activate_overtime_allowance', 'activate_leave_allowance', 'overtime','leave_allowance','lateness','absence','damage','total_dedcutions', 'total_allowances', 'net_pay_after_ed')   

admin.site.register(Department)
admin.site.register(Grade)
admin.site.register(Company)
admin.site.register(Payroll)
admin.site.register(User)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(DeductionsAndEarnings, DeductionsAndEarningsAdmin)



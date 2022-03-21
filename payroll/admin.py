from django.contrib import admin

from payroll.models import Department, Grade, Payroll, Employee, DeductionsAndEarnings, Company, Base_payroll

from import_export import resources
from import_export.admin import ImportExportModelAdmin

class EmployeeResource(resources.ModelResource):

    class Meta:
        model = Employee
class PayrollResource(resources.ModelResource):

    class Meta:
        model = Payroll
class GradeResource(resources.ModelResource):

    class Meta:
        model = Grade
class EDResource(resources.ModelResource):

    class Meta:
        model = DeductionsAndEarnings
class EmployeeAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ('Employee_id', 'bank','department', 'first_name', 'bank_account','net_pay')

class DeductionsAndEarningsAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ('id','employee', 'lateness_deduction', 'absence_deduction', 'activate_overtime_allowance', 'activate_leave_allowance', 'overtime','leave_allowance','lateness','absence','damage','total_dedcutions', 'total_allowances', 'net_pay_after_ed')
    list_display_links = ('employee',)
    list_editable = ('lateness_deduction', 'absence_deduction', 'activate_overtime_allowance', 'activate_leave_allowance', 'overtime','leave_allowance','lateness','absence','damage','total_dedcutions', 'total_allowances', 'net_pay_after_ed')   

admin.site.register(Department, ImportExportModelAdmin)
admin.site.register(Grade, ImportExportModelAdmin)
admin.site.register(Company, ImportExportModelAdmin)
admin.site.register(Payroll, ImportExportModelAdmin)
admin.site.register(Base_payroll, ImportExportModelAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(DeductionsAndEarnings, DeductionsAndEarningsAdmin)




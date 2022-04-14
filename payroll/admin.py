from django.contrib import admin

from payroll.models import Department, Grade, Payroll, Employee, DeductionsAndEarnings, Company, BasePayroll

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



admin.site.register(Department, ImportExportModelAdmin)
admin.site.register(Grade, ImportExportModelAdmin)
admin.site.register(Company, ImportExportModelAdmin)
admin.site.register(Payroll, ImportExportModelAdmin)
admin.site.register(Employee)





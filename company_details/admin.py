from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Employee, Contact, Payroll

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('city', 'phone_number', 'employee_code')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('city', 'phone_number', 'employee_code')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Employee)
admin.site.register(Contact)
admin.site.register(Payroll)

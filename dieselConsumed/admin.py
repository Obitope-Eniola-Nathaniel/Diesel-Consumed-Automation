from django.contrib import admin
from .models import User, Tenant, GeneratorUsage
# Register your models here.

admin.site.register(User)


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit')

@admin.register(GeneratorUsage)
class GeneratorUsageAdmin(admin.ModelAdmin):
    list_display = ('tenant', 'date', 'hours_used', 'price_per_hour', 'calculate_amount')
    list_filter = ('date', 'tenant')
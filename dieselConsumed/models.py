from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now
from django.db.models import Sum


class User(AbstractUser):
    pass


class Tenant(models.Model):
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=50, unique=True)  # E.g., Apartment/Unit ID

    def __str__(self):
        return self.name


class GeneratorUsage(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="usages")
    date = models.DateField(default=now)
    hours_used = models.DecimalField(max_digits=5, decimal_places=2)
    price_per_hour = models.DecimalField(max_digits=7, decimal_places=2)

    class Meta:
        unique_together = ('tenant', 'date')  # Prevent duplicate entries for the same day.

    def calculate_amount(self):
        return self.hours_used * self.price_per_hour

    def __str__(self):
        return f"{self.tenant.name} - {self.date}"

    @classmethod
    def calculate_monthly_usage(cls, tenant_id, year, month):
        records = cls.objects.filter(tenant_id=tenant_id, date__year=year, date__month=month)
        total_hours = records.aggregate(Sum('hours_used'))['hours_used__sum'] or 0
        total_amount = sum(record.calculate_amount() for record in records)
        return {
            "month": month,
            "year": year,
            "total_hours": total_hours,
            "total_amount": total_amount,
        }
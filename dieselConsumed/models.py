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


class DailyRecord(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="daily_records")
    date = models.DateField(default=now)
    hours_used = models.DecimalField(max_digits=5, decimal_places=2)
    price_per_hour = models.DecimalField(max_digits=7, decimal_places=2)

    class Meta:
        unique_together = ('tenant', 'date')  # Prevent duplicate entries for the same day.

    def calculate_amount(self):
        return self.hours_used * self.price_per_hour

    def __str__(self):
        return f"{self.tenant.name} - {self.date}"

   

class MonthlySummary(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='monthly_summaries')
    year = models.IntegerField()
    month = models.IntegerField()
    total_hours = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.tenant.name} - {self.month}/{self.year}"

    @classmethod
    def generate_monthly_summary(cls, tenant, year, month):
        # Calculate totals from DailyRecord
        daily_records = DailyRecord.objects.filter(
            tenant=tenant, date__year=year, date__month=month
        )
        total_hours = daily_records.aggregate(Sum('hours_used'))['hours_used__sum'] or 0
        total_amount = sum(record.daily_amount for record in daily_records)

        # Create or update MonthlySummary
        summary, created = cls.objects.update_or_create(
            tenant=tenant, year=year, month=month,
            defaults={'total_hours': total_hours, 'total_amount': total_amount}
        )
        return summary
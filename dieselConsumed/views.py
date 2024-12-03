from django.shortcuts import HttpResponse, HttpResponseRedirect, render, get_object_or_404
from django.urls import reverse
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from datetime import datetime

from .models import User, Tenant, GeneratorUsage
# Create your views here.


def tenant_monthly_usage(request, tenant_id, year, month):
    tenant = get_object_or_404(Tenant, id=tenant_id)
    summary = GeneratorUsage.calculate_monthly_usage(tenant_id, year, month)

    return render(request, 'dieselConsumed/tenant_summary.html', {
        'tenant': tenant,
        'summary': summary
    })


def index(request):

    # Authenticated users view their inbox
    if request.user.is_authenticated:
        tenants = Tenant.objects.all()
        genUsed = GeneratorUsage.objects.all()

        return render(request, 'dieselConsumed/index.html', {
            'tenants': tenants,
            'genUsed': genUsed 
        })

    # Everyone else is prompted to sign in
    else:
        return HttpResponseRedirect(reverse("login"))


# Display Listing Based on Cetegory
def displayTenant(request, id):
    tenant = Tenant.objects.get(id=id)
    tenantGeneratorUsage = GeneratorUsage.objects.filter(tenant=tenant)
    current_date = datetime.now()

    return render(request, "dieselConsumed/tenantDisplay.html", {
        "tenantBill": tenantGeneratorUsage,
        'tenant': tenant,
        'year': current_date.year,
        'month': current_date.month,
    })
    
# Add Tenant
def addTenant(request):
    tenants = Tenant.objects.all()
    if request.method == "POST":
        tenant = request.POST["tenant"]
        unit = request.POST["unit"]

        if tenant in tenants or unit in tenants:
            return
        
        tenant = Tenant(name=tenant, unit=unit)
        tenant.save()
        return HttpResponseRedirect(reverse("index"))


# Add Tenant Consumtion
def addTenantConsumption(request, id):
    tenants = Tenant.objects.get(id=id)
    # tenantsConsumed = GeneratorUsage.objects.get(tenant=id)
    if request.method == "POST":
        dieselHrs = request.POST["dieselHrs"]
        amount = request.POST["amount"]

        
        consume = GeneratorUsage(tenant=tenants, hours_used=dieselHrs, price_per_hour=amount)
        consume.save()
        return HttpResponseRedirect(reverse("displayTenant", args=(id,)))
          
# Delete Tenant Cosumption
def delete_consume(request, id):
    consumed = GeneratorUsage.objects.get(id=id)
    consumed.delete()
    return HttpResponseRedirect(reverse("displayTenant", args=(id,)))
    # return render(request,'myapp/delete.html')

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "dieselConsumed/login.html", {
                "message": "Invalid email and/or password."
            })
    else:
        return render(request, "dieselConsumed/login.html")
    

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "dieselConsumed/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(email, email, password)
            user.save()
        except IntegrityError as e:
            print(e)
            return render(request, "mail/register.html", {
                "message": "Email address already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "dieselConsumed/register.html")

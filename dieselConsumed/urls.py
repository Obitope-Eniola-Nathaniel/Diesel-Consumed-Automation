from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),

    path('tenant/<int:tenant_id>/<int:year>/<int:month>/', views.tenant_monthly_usage, name='tenant_monthly_usage'),
    path('displayTenant/<int:id>', views.displayTenant, name="displayTenant"),
    path('addTenant', views.addTenant, name="addTenant"),
    path('addTenantConsumption/<int:id>', views.addTenantConsumption, name="addTenantConsumption"),
    path('delete/<int:id>/', views.delete_consume,name="delete"),
]

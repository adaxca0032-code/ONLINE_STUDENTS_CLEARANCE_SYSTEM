"""
URL configuration for core project.
"""
from django.contrib import admin
from django.urls import path, include  # Hakikisha 'include' ipo hapa

urlpatterns = [
    # 1. Mlango wa Admin wa Django (Ule wa default)
    path('admin/', admin.site.urls),
    
    # 2. Huu mstari unaunganisha kurasa zote za clearance_app (Login na Dashboards)
    path('', include('clearance_app.urls')),
]
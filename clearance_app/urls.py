from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # 1. Njia kuu ya mfumo (Inachuja kama ni mwanafunzi au afisa na kumuelekeza sehemu husika)
    path('', views.dashboard_redirect_view, name='dashboard_redirect'),
    
    # 2. Ukurasa wa Login (Tumerekebisha folda liwe 'dashboard/login.html' ili lilingane na folda lako)
    path('login/', auth_views.LoginView.as_view(template_name='dashboard/login.html'), name='login'),
    
    # 3. Ukurasa wa Logout (Tumeweka next_page ili ikubali kumtupa mteja kwenye login mara tu anapo-logout)
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    
    # 4. Dashboard ya Mwanafunzi (Student Portal)
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    
    # 5. Dashboard ya Afisa wa Idara (Finance, Library, ICT, nk.)
    path('officer/dashboard/', views.officer_dashboard, name='officer_dashboard'),
]
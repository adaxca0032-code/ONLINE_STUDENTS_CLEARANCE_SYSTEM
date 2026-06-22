from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from . import views

# === MBINU YA KUTENGEZA ADMIN MTANDAONI BILA TERM_INAL YA RENDER ===
def tengeneza_admin_wa_render(request):
    User = get_user_model()
    # Inakagua kama user huyu hayupo mtandaoni, ndipo inamtengeneza
    if not User.objects.filter(username='admin_online').exists():
        User.objects.create_superuser('admin_online', 'admin@example.com', 'Mussa@2026')
        return HttpResponse("Hongera Skillfully Man! Akaunti ya 'admin_online' imetengenezwa mtandaoni!")
    return HttpResponse("Akaunti ya 'admin_online' tayari ipo mtandaoni!")


urlpatterns = [
    # Njia ya mkato ya kutengeneza akaunti ya admin kule Render (Ibonyeze mara moja tu ukiwa mtandaoni)
    path('tengeneza-admin/', tengeneza_admin_wa_render, name='tengeneza_admin_wa_render'),

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
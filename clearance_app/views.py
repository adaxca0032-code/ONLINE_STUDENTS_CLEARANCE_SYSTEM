import datetime  # Nyongeza: Muhimu kwa ajili ya kuzalisha miaka dynamically
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserProfile, ClearanceRequest, DepartmentalApproval

@login_required
def dashboard_redirect_view(request):
    """
    Inamwelekeza mtumiaji kwenye dashboard husika kulingana na jukumu lake (Role).
    """
    try:
        profile = request.user.userprofile
        if profile.role == 'student':
            return redirect('student_dashboard')
        elif profile.role == 'officer':
            return redirect('officer_dashboard')
        elif profile.role == 'registrar':
            return redirect('registrar_dashboard')
    except UserProfile.DoesNotExist:
        # Ikitokea akaunti haina wasifu (UserProfile), inamrudisha kwenye login safi
        return redirect('login')
    
    return redirect('login')


@login_required
def student_dashboard(request):
    """
    Dashboard ya Mwanafunzi: Kuona hali ya clearance na kutuma maombi mapya dynamically.
    """
    # Hakikisha ni mwanafunzi kweli
    if request.user.userprofile.role != 'student':
        return redirect('dashboard_redirect')
        
    profile = request.user.userprofile
    
    # KUZALISHA MIAKA DYNAMICALLY:
    # Inasoma mwaka wa sasa wa kalenda (kama ni 2026, itasoma 2026)
    current_year = datetime.date.today().year
    
    # Inatengeneza muundo wa miaka ya masomo ya chuo (Academic Years kama '2025/2026', '2026/2027')
    # Loop hii inatengeneza miaka miwili ya nyuma na miaka minne ya mbele
    years_range = []
    for y in range(current_year - 2, current_year + 4):
        next_year = y + 1
        academic_format = f"{y}/{next_year}"  # Inazalisha mfumo wa "2025/2026"
        years_range.append(academic_format)
        
    # Kupata ombi la mwisho la mwanafunzi huyu
    current_request = ClearanceRequest.objects.filter(student=request.user).order_by('-created_at').first()
    
    approvals = []
    if current_request:
        approvals = DepartmentalApproval.objects.filter(request=current_request)
        
    if request.method == 'POST':
        if current_request and current_request.get_status() == 'Pending':
            messages.warning(request, "Tayari una ombi linalofanyiwa kazi kwa sasa.")
            return redirect('student_dashboard')
            
        # SULUHISHO: Inasoma uwanja uliochaguliwa na mwanafunzi, isipoupa inaweka mwaka wa sasa kama backup
        default_academic_format = f"{current_year}/{current_year + 1}"
        academic_year = request.POST.get('academic_year', default_academic_format)
        reason = request.POST.get('reason', 'Graduation')
        
        # Kutengeneza ombi kuu jipya la clearance
        new_request = ClearanceRequest.objects.create(
            student=request.user,
            academic_year=academic_year,  # Hifadhi ule mwaka uliochaguliwa dynamic
            reason=reason
        )
        
        # Mfumo unajigawa kiotomatiki kwenda kwenye Idara kuu 3
        departments = ['Library', 'Finance', 'ICT']
        for dept in departments:
            DepartmentalApproval.objects.create(
                request=new_request,
                department=dept,
                status='Pending'
            )
            
        messages.success(request, "Ombi lako la clearance limetumwa kikamilifu kwenye idara zote!")
        return redirect('student_dashboard')
        
    context = {
        'profile': profile,
        'current_request': current_request,
        'approvals': approvals,
        'years_range': years_range,        # Nyongeza: Imetumwa ili HTML iweze kuizungusha (loop)
        'current_academic_year': f"{current_year}/{current_year + 1}" # Inatumika kuweka pre-selected chaguo la sasa
    }
    return render(request, 'dashboard/student.html', context)


@login_required
def officer_dashboard(request):
    """
    Dashboard ya Maafisa wa Idara: Kuona na kuidhinisha (Approve/Reject) maombi ya idara zao pekee.
    """
    if request.user.userprofile.role != 'officer':
        return redirect('dashboard_redirect')
        
    profile = request.user.userprofile
    officer_dept = profile.department  # Mfano: 'Library', 'Finance', au 'ICT'
    
    # Kuchuja maombi yanayohusu idara hii tu
    pending_approvals = DepartmentalApproval.objects.filter(department=officer_dept, status='Pending').select_related('request__student')
    history_approvals = DepartmentalApproval.objects.filter(department=officer_dept).exclude(status='Pending').select_related('request__student')
    
    if request.method == 'POST':
        approval_id = request.POST.get('approval_id')
        action = request.POST.get('action')  # 'Approved' au 'Rejected'
        comments = request.POST.get('comments', '')
        
        approval = get_object_or_404(DepartmentalApproval, id=approval_id, department=officer_dept)
        approval.status = action
        approval.comments = comments
        approval.actioned_by = request.user
        approval.save()
        
        messages.success(request, f"Ombi limeidhinishwa kama: {action}")
        return redirect('officer_dashboard')
        
    context = {
        'profile': profile,
        'pending_approvals': pending_approvals,
        'history_approvals': history_approvals
    }
    return render(request, 'dashboard/officer.html', context)


@login_required
def registrar_dashboard(request):
    """
    Dashboard ya Msajili (Registrar): Kuona hali ya mwisho ya wanafunzi wote waliofanya clearance.
    """
    if request.user.userprofile.role != 'registrar':
        return redirect('dashboard_redirect')
        
    profile = request.user.userprofile
    all_requests = ClearanceRequest.objects.all().order_by('-created_at').select_related('student')
    
    context = {
        'profile': profile,
        'all_requests': all_requests
    }
    return render(request, 'dashboard/registrar.html', context)
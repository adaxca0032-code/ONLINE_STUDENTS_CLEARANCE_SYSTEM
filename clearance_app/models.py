from django.db import models
from django.contrib.auth.models import User

# 1. Meza ya UserProfile (Wasifu wa Watumiaji)
class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('officer', 'Officer'),
        ('registrar', 'Registrar'),  # Tumeongeza na Registrar kwa usalama wa baadae
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=15, choices=ROLE_CHOICES)
    department = models.CharField(max_length=50, blank=True, null=True)  # Mfano: Library, Finance, ICT

    def __str__(self):
        return f"{self.user.username} - {self.role}"


# 2. Meza ya ClearanceRequest (Ombi Kuu la Mwanafunzi)
class ClearanceRequest(models.Model):
    REASON_CHOICES = [
        ('graduation', 'Graduation'),
        ('withdrawal', 'Studies Withdrawal'),
        ('postponement', 'Postponement'),
    ]
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    academic_year = models.CharField(max_length=20)
    reason = models.CharField(max_length=20, choices=REASON_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request by {self.student.username}"

    def get_status(self):
        """
        Inakagua hali ya sasa ya ombi hili kwa kuangalia idara zote 3.
        Hii ndio iliyokuwa inasababisha AttributeError!
        """
        approvals = self.approvals.all()  # Inatumia related_name='approvals'
        if not approvals.exists():
            return "Pending"
            
        # Kama kuna idara hata moja imekataa
        if any(app.status == 'Rejected' for app in approvals):
            return "Rejected"
            
        # Kama idara zote 3 zimekubali (Approved)
        if all(app.status == 'Approved' for app in approvals):
            return "Approved"
            
        return "Pending"


# 3. Meza ya DepartmentalApproval (Idhini za Idara Moja Moja)
class DepartmentalApproval(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    request = models.ForeignKey(ClearanceRequest, on_delete=models.CASCADE, related_name='approvals')
    department = models.CharField(max_length=50)  # Mfano: Library, Finance, ICT
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Pending')
    comments = models.TextField(blank=True, null=True)  # Tulirekebisha kutoka remarks kwenda comments
    actioned_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='officer_actions')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.department} - {self.status}"
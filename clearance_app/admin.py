from django.contrib import admin
from .models import UserProfile, ClearanceRequest, DepartmentalApproval

# 1. Kusajili UserProfile ili uweze kutoa Roles za Student au Officer
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'department')
    list_filter = ('role', 'department')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')

# 2. Kusajili ClearanceRequest (Maombi ya wanafunzi)
@admin.register(ClearanceRequest)
class ClearanceRequestAdmin(admin.ModelAdmin):
    list_display = ('student', 'academic_year', 'reason', 'created_at')
    list_filter = ('academic_year', 'reason')
    search_fields = ('student__username',)

# 3. Kusajili DepartmentalApproval (Zile idara zinazopitisha)
@admin.register(DepartmentalApproval)
class DepartmentalApprovalAdmin(admin.ModelAdmin):
    list_display = ('request', 'department', 'status', 'updated_at')
    list_filter = ('department', 'status')
    search_fields = ('request__student__username', 'remarks')
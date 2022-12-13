"""
Admin view for the application.
"""
from django.contrib import admin

from lessons.models import BankTransfer, Lesson, Request, User
from .models import *
from .forms import CustomUserCreationForm

# Register your models here.

class BaseAdmin():
    
    def is_user_allowed(self, request):
        return request.user.is_staff

    def has_change_permission(self, request, obj = None):
        return self.is_user_allowed(request)
    
    def has_delete_permission(self, request, obj=None):
        return self.is_user_allowed(request)

    def has_add_permission(self, request, obj=None):
        return self.is_user_allowed(request)

    def has_view_permission(self, request, obj=None):
        return self.is_user_allowed(request)

    def has_module_permission(self, request, obj=None):
        return self.is_user_allowed(request)

class LessonInline(BaseAdmin, admin.TabularInline):
    model = Lesson

@admin.register(User)
class StudentAdmin(BaseAdmin, admin.ModelAdmin):
    """ Admin view for the User model. """
    add_form = CustomUserCreationForm
    model = User
    list_display = [
        "email", "first_name", "last_name", "is_staff", "is_superuser"
    ]
    
    def has_change_permission(self, request, obj = None):
        if obj and (obj.is_superuser or obj.is_staff):
            return False
        return True
    
    def has_delete_permission(self, request, obj=None):
        if obj and (obj.is_superuser or obj.is_staff):
            return False
        return True

    def has_add_permission(self, request, obj=None):
        if obj and (obj.is_superuser or obj.is_staff):
            return False
        return True

    def get_readonly_fields(self, request, obj = None):
        if request.user.is_staff:
            if request.user.is_superuser:
                return []
            return ["is_superuser", "is_staff"]

class pendingRequest(Request):
    class Meta:
        proxy = True
        verbose_name = "Pending Request"

class approvedRequest(Request):
    class Meta:
        proxy = True
        verbose_name = "Fulfilled Request"

@admin.register(pendingRequest)
class pendingRequestAdmin(BaseAdmin, admin.ModelAdmin):
    """ Admin view for requests that have not been approved yet. """
    def get_queryset(self, request):
        return Request.objects.filter(is_approved = False)
    
    @admin.display(description="Request info")
    def request_info(self, obj):
        return f'Request-{obj.id}'

    list_display = [
       "request_info", "user", "is_approved"
    ]
    readonly_fields = ["is_approved"]
    inlines = [LessonInline]
        
@admin.register(approvedRequest)
class approvedRequestAdmin(BaseAdmin, admin.ModelAdmin):
    """ Admin view for requests that have been approved. """
    def get_queryset(self, request):
        return Request.objects.filter(is_approved = True)
    
    @admin.display(description="Request info")
    def request_info(self, obj):
        return f'Request-{obj.id}'

    list_display = [
       "request_info", "user", "is_approved"

    ]
    readonly_fields = ["is_approved"]
    inlines = [LessonInline]

@admin.register(BankTransfer)
class BankTransferAdmin(BaseAdmin, admin.ModelAdmin):
    """ Admin view for bank transfers. """
    list_display = [
        "user", "lesson","invoice_number", "cost"
    ]


@admin.register(Lesson)
class LessonAdmin(BaseAdmin, admin.ModelAdmin):
    """ Admin view for lessons. """

    @admin.display(description="Student")
    def user_name(self, obj):
        return obj.request.user

    list_display = ["request", "teacher", "user_name", "startDate", "paid"]
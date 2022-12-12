"""
Admin view for the application.
"""
from django.contrib import admin

from lessons.models import BankTransfer, Lesson, Request, User
from .models import *
from .forms import CustomUserCreationForm, CustomUserChangeForm

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """ Admin view for the User model. """
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = [
        "email", "first_name", "last_name", "is_staff", "is_superuser"
    ]

class LessonInline(admin.TabularInline):
    model = Lesson

class pendingRequest(Request):
    class Meta:
        proxy = True
        verbose_name = "Pending Request"

class approvedRequest(Request):
    class Meta:
        proxy = True
        verbose_name = "Fulfilled Request"

@admin.register(pendingRequest)
class pendingRequestAdmin(admin.ModelAdmin):
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
class approvedRequestAdmin(admin.ModelAdmin):
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
class BankTransferAdmin(admin.ModelAdmin):
    """ Admin view for bank transfers. """
    list_display = [
        "user", "lesson","invoice_number", "full_invoice_number", "cost"
    ]

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    """ Admin view for lessons. """

    @admin.display(description="Student")
    def user_name(self, obj):
        return obj.request.user

    list_display = ["request", "teacher", "user_name", "startDate", "paid"]


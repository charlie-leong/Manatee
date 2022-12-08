"""
Admin view for the application.
"""
from django.contrib import admin

from lessons.models import BankTransfer, Lesson, Request, User
# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """ Admin view for the User model. """
    list_display = [
        "username", "first_name", "last_name", "email", "is_staff", "is_superuser"
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
        return f'request-{obj.id}'

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
        return f'request-{obj.id}'

    list_display = [
       "request_info", "user", "is_approved"
    ]
    readonly_fields = ["is_approved"]
    inlines = [LessonInline]

@admin.register(BankTransfer)
class BankTransferAdmin(admin.ModelAdmin):
    """ Admin view for bank transfers. """
    list_display = [
        "user_ID", "invoice_number", "full_invoice_number", "pay", "paid"
    ]

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    """ Admin view for lessons. """
    list_display = ["request", "teacher", "startDate", "paid"]
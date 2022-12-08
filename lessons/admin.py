from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
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
    def get_queryset(self, request):
        return Request.objects.filter(is_approved = False)
    list_display = [
       "id", "user", "availability", "number_of_lessons", "interval", "duration", "is_approved"
    ]
    readonly_fields = ["is_approved"]
    inlines = [LessonInline]
        
@admin.register(approvedRequest)
class approvedRequestAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return Request.objects.filter(is_approved = True)
    list_display = [
       "id", "user", "availability", "number_of_lessons", "interval", "duration", "is_approved"
    ]
    readonly_fields = ["is_approved"]
    inlines = [LessonInline]

@admin.register(BankTransfer)
class BankTransferAdmin(admin.ModelAdmin):
    list_display = [
        "user_ID", "invoice_number", "full_invoice_number", "pay", "paid"
    ]

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ["request", "teacher", "paid"]
from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        "username", "first_name", "last_name", "email", "is_staff", "is_superuser"
    ]

@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = [
        "availability", "number_of_lessons", "interval", "duration", "extra_info", "created_by", "is_approved"
    ]

@admin.register(BankTransfer)
class BankTransferAdmin(admin.ModelAdmin):
    list_display = [
        "user_ID", "invoice_number", "full_invoice_number", "pay", "paid"
    ]

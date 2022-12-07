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

@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
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
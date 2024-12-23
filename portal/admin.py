from django.contrib import admin
from .models import Company, User
import random

@admin.register(User)
class UserAdmin(admin.ModelAdmin):    
    list_display = ["email", "first_name", "last_name", "is_active", "is_staff", "is_superuser"]
    list_filter = ["is_active", "is_staff", "is_superuser"]
    search_fields = ["email", "first_name", "last_name"]
    ordering = ["email"]
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    
    # reset password action
    actions = ["reset_password"]
    
    def reset_password(self, request, queryset):
        """Reset password for selected users"""
        #  get 8 random characters
        new_password = "".join(random.choices("abcdefghijklmnopqrstuvwxyz1234567890", k=8))
        for user in queryset:
            user.set_password(new_password)
            user.save()
        self.message_user(request, "Password reset successfully, new password is: {}".format(new_password))
    
            
    
    
    def get_readonly_fields(self, request, obj=None):
        """Make password field read-only"""
        if obj:
            return ["password", "last_login", "date_joined"]
        else:
            return ["last_login", "date_joined"]

    def save_model(self, request, obj, form, change):
        """Set password for new users"""
        obj.set_password(obj.password)
        super().save_model(request, obj, form, change)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ["name", "address", "phone", "email", "website", "created_at", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["name", "address", "phone", "email", "website"]
    ordering = ["name"]


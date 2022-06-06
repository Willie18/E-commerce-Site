from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomerUser
# Register your models here.

class UserAdminConfig(UserAdmin):
    ordering=('-created_at',)
    list_display=("email","username","is_active","is_staff")
    search_fields=("email","username",)
    
    add_fieldsets = (
    (None, {
        'fields': ('username', 'email', 'is_staff', 'is_active',),
    }),
       )

admin.site.register(CustomerUser,UserAdminConfig)

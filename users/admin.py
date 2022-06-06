from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomerUser
# Register your models here.

class UserAdminConfig(UserAdmin):
    ordering=('-created_at',)
    list_display=("email","username","is_active","is_staff",)
    search_fields=("email","username",)
    add_fieldsets = (
        (None, {'fields': ('email', 'username', 'is_active',  'is_staff',)}),
    )
    fieldsets = (
        (None, {
            "fields": (
                ('email', 'username', 'is_active', 'is_staff',)
                
            ),
        }),
    )

admin.site.register(CustomerUser,UserAdminConfig)

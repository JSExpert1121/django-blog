from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.


class CustomAdmin(UserAdmin):
    list_display = ('first_name', 'last_name',
                    'date_joined', 'last_login', 'is_admin')
    readonly_fields = ('date_joined', 'last_login')

    filter_horizontal = ()
    ordering = ('date_joined',)
    list_filter = ()
    fieldsets = ()

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )


admin.site.register(User, CustomAdmin)

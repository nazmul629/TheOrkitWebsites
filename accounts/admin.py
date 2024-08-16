from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account

class AccountAdmin(UserAdmin):
    list_display = ('email','first_name','last_name','phone_number','date_joined','last_login','is_active')

    list_display_links = ('email','first_name','last_name')

    readonly_fields = ('date_joined','last_login')
    ordering=('-date_joined',)

    filter_horizontal=()
    list_filter=()
    fieldsets = ()

# Register your models here.
admin.site.register(Account,AccountAdmin)
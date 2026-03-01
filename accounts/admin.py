from django.contrib import admin
from .models import WebUser, Admin


@admin.register(WebUser)
class WebUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'usertype')
    list_filter = ('usertype',)
    search_fields = ('email',)


@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('aemail', 'apassword')

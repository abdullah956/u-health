from django.contrib import admin
from .models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('pid', 'pname', 'pemail', 'ptel', 'pdob')
    search_fields = ('pname', 'pemail__email')

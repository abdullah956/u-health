from django.contrib import admin
from .models import Doctor, Specialties


@admin.register(Specialties)
class SpecialtiesAdmin(admin.ModelAdmin):
    list_display = ('id', 'sname')
    search_fields = ('sname',)


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('docid', 'docname', 'docemail', 'doctel', 'specialties')
    search_fields = ('docname', 'docemail__email')
    list_filter = ('specialties',)

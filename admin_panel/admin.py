from django.contrib import admin
from .models import Schedule, Appointment


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('scheduleid', 'title', 'docid', 'scheduledate', 'scheduletime', 'nop')
    list_filter = ('scheduledate', 'docid')
    search_fields = ('title', 'docid__docname')


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('appoid', 'pid', 'scheduleid', 'appodate', 'apponum')
    list_filter = ('appodate',)
    search_fields = ('pid__pname',)

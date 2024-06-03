'''from django.contrib import admin
from django_celery_beat.models import PeriodicTask, IntervalSchedule

@admin.register(IntervalSchedule)
class IntervalScheduleAdmin(admin.ModelAdmin):
    list_display = ('every', 'period')'''

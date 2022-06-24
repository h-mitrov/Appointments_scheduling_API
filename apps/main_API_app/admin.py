from django.contrib import admin
from .models import Location, Worker, Client, Schedule, Appointment


# Register your models here.
admin.site.register(Client)
admin.site.register(Schedule)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('type',
                    'worker',
                    'location',
                    'client',
                    'date',
                    'start_time',
                    'end_time',
                    )


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    exclude = ('schedule_ids',)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    exclude = ('schedule_ids',)

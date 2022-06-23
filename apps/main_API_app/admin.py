from django.contrib import admin
from .models import Location, Worker, Client, Schedule, Appointment


# Register your models here.
admin.site.register(Location)
admin.site.register(Worker)
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

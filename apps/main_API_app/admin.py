# Third party imports
from django.contrib import admin

# Local app imports
from .models import Location, Worker, Client, Schedule, Appointment


# Register your models here.
admin.site.register(Client)
admin.site.register(Schedule)
admin.site.register(Worker)
admin.site.register(Location)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    """
    Class for customizing Appointment model in the admin panel.
    """
    list_display = ('type',
                    'worker',
                    'location',
                    'client',
                    'date',
                    'start_time',
                    'end_time',
                    )

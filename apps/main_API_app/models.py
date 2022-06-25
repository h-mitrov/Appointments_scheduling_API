from datetime import datetime, timedelta

import django.utils.timezone
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q, ObjectDoesNotExist


class Schedule(models.Model):
    weekdays = [
        (1, "Monday"),
        (2, "Tuesday"),
        (3, "Wednesday"),
        (4, "Thursday"),
        (5, "Friday"),
        (6, "Saturday"),
        (7, "Sunday"),
    ]

    weekday = models.IntegerField(choices=weekdays, default='Monday')
    from_hour = models.TimeField()
    to_hour = models.TimeField()

    def __str__(self):
        return f'{self.weekdays[self.weekday - 1][1]}: {self.from_hour}—{self.to_hour}'

    class Meta:
        ordering = ('weekday', 'from_hour')
        unique_together = ('weekday', 'from_hour', 'to_hour')

    def __unicode__(self):
        return u'%s: %s - %s' % (self.get_weekday_display(),
                                 self.from_hour, self.to_hour)


class Location(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField(max_length=600)
    schedule_ids = models.JSONField(default='1', blank=True)
    work_schedule = models.ManyToManyField(Schedule, blank=True)

    class Meta:
        unique_together = ('name', 'address')

    def __str__(self):
        return f'{self.name} ({self.address})'


class Worker(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)
    schedule_ids = models.JSONField(default='1', blank=True)
    work_schedule = models.ManyToManyField(Schedule, blank=True)

    class Meta:
        unique_together = ('first_name', 'last_name', 'specialty')

    def __str__(self):
        return f'{self.specialty} — {self.first_name} {self.last_name}'


class Client(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Appointment(models.Model):
    type = models.CharField(max_length=100, blank=False)
    date = models.DateField(default=django.utils.timezone.localdate, blank=False)
    start_time = models.TimeField(default=django.utils.timezone.localtime, blank=False)
    end_time = models.TimeField(blank=False)
    worker = models.ForeignKey('Worker', on_delete=models.CASCADE, blank=False)
    client = models.ForeignKey('Client', on_delete=models.CASCADE, blank=False)
    location = models.ForeignKey('Location', on_delete=models.CASCADE, blank=False)

    def clean(self):
        try:
            # check that start is before finish
            if self.start_time >= self.end_time:
                raise ValidationError({"end_time": f"Can't book. Procedure end time must occur after start."})

            # check if location and worker can be booked at certain day and time range
            for parameter in self.location, self.worker:
                schedule_match = False

                if parameter is self.location:
                    schedules_for_checking = Schedule.objects.filter(location=self.location)
                    print(schedules_for_checking)
                else:
                    schedules_for_checking = Schedule.objects.filter(worker=self.worker)

                current_weekday = self.date.weekday() + 1

                for schedule in schedules_for_checking:
                    condition = all((schedule.weekday == current_weekday,
                                     schedule.from_hour <= self.start_time < schedule.to_hour,
                                     schedule.from_hour < self.end_time <= schedule.to_hour
                                     ))
                    print(schedule.weekday == current_weekday)
                    print(schedule.weekday)
                    print(schedule.from_hour <= self.start_time < schedule.to_hour)
                    print(schedule.from_hour < self.end_time <= schedule.to_hour)

                    if condition:
                        schedule_match = True

                if not schedule_match:
                    raise ValidationError({"date": f"Can't book. The {parameter} can't be assigned an appointment"
                                                                         f" at this day and time"})

            # check if location and worker are not already booked at certain day and time
            similar_appointments = Appointment.objects.filter(Q(date=self.date),
                                                              Q(start_time__lte=self.start_time,
                                                                end_time__gte=self.start_time) |
                                                              Q(start_time__lte=self.end_time,
                                                                end_time__gte=self.end_time) |
                                                              Q(start_time__range=(self.start_time, self.end_time)) |
                                                              Q(end_time__range=(self.start_time, self.end_time))
                                                              )
            print(similar_appointments)
            if similar_appointments.exists():
                for appointment in similar_appointments:
                    if self.worker == appointment.worker:
                        raise ValidationError({"worker": f"Can't book. The {self.worker} specialist is"
                                                                     f" already booked at this time"})
                    if self.location == appointment.location:
                        raise ValidationError({"location": f"Can't book. The {self.location} location is"
                                                         f" already booked at this time"})
                    if self.client == appointment.client:
                        raise ValidationError({"client": f"Can't book. The {self.client} client already has"
                                                         f" an appointment at this time"})

        except ObjectDoesNotExist:
            raise ValidationError('Please, fill all of the fields.')

    def __str__(self):
        return f'{self.type} ({self.client})'

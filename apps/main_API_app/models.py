from datetime import datetime, timedelta

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q, ObjectDoesNotExist


class Location(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField(max_length=600)

    def __str__(self):
        return f'{self.name} ({self.address})'


class Schedule(models.Model):
    WEEKDAYS = [
        (1, "Monday"),
        (2, "Tuesday"),
        (3, "Wednesday"),
        (4, "Thursday"),
        (5, "Friday"),
        (6, "Saturday"),
        (7, "Sunday"),
    ]

    weekday = models.IntegerField(choices=WEEKDAYS, default='Monday')
    from_hour = models.TimeField()
    to_hour = models.TimeField()

    def __str__(self):
        return f'{self.WEEKDAYS[self.weekday - 1][1]}: {self.from_hour}—{self.to_hour}'

    class Meta:
        ordering = ('weekday', 'from_hour')
        unique_together = ('weekday', 'from_hour', 'to_hour')

    def __unicode__(self):
        return u'%s: %s - %s' % (self.get_weekday_display(),
                                 self.from_hour, self.to_hour)


class Worker(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)
    work_schedule = models.ManyToManyField(Schedule)

    def __str__(self):
        return f'{self.specialty} — {self.first_name} {self.last_name}'


class Client(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Appointment(models.Model):
    current_time = datetime.now()

    type = models.CharField(max_length=100, blank=False)
    date = models.DateField(default=current_time.date(), blank=False)
    start_time = models.TimeField(default=current_time.time(), blank=False)
    end_time = models.TimeField(default=(datetime.now() + timedelta(hours=1)), blank=False)
    worker = models.ForeignKey('Worker', on_delete=models.CASCADE, blank=False)
    client = models.ForeignKey('Client', on_delete=models.CASCADE, blank=False)
    location = models.ForeignKey('Location', on_delete=models.CASCADE, blank=False)

    def clean(self):
        try:
            worker_schedules = Schedule.objects.filter(worker=self.worker)
            current_weekday = self.date.weekday()
            schedule_match = False

            for schedule in worker_schedules:
                condition = all((schedule.weekday == current_weekday,
                                 schedule.from_hour <= self.start_time < schedule.to_hour,
                                 schedule.from_hour < self.end_time <= schedule.to_hour
                                 ))
                if condition:
                    schedule_match = True
                    break

            if not schedule_match:
                raise ValidationError({"worker": f"Can't book. The {self.worker} specialist doesn't receive clients"
                                                                     f" at this day and time"})

            similar_appointments = Appointment.objects.filter(Q(date=self.date),
                                                              Q(start_time__lte=self.start_time,
                                                                end_time__gte=self.start_time) |
                                                              Q(start_time__lte=self.end_time,
                                                                end_time__gte=self.end_time) |
                                                              Q(start_time__range=(self.start_time, self.end_time)) |
                                                              Q(end_time__range=(self.start_time, self.end_time))
                                                              )

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

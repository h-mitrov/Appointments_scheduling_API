import datetime

from django.db import models

WEEKDAYS = [
  (1, "Monday"),
  (2, "Tuesday"),
  (3, "Wednesday"),
  (4, "Thursday"),
  (5, "Friday"),
  (6, "Saturday"),
  (7, "Sunday"),
]


class Location(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField(max_length=600)
    bookings = models.JSONField(default=dict(date="hour"))

    def __str__(self):
        return f'{self.name} ({self.address})'


class Schedule(models.Model):
    # default_range = [9, 18]
    # default_schedule = {"monday": default_range,
    #                     "tuesday": default_range,
    #                     "wednesday": default_range,
    #                     "thursday": default_range,
    #                     "friday": default_range,
    #                     "saturday": default_range,
    #                     "sunday": default_range
    #                     }

    weekday = models.IntegerField(choices=WEEKDAYS, default='Monday')
    from_hour = models.TimeField()
    to_hour = models.TimeField()

    def __str__(self):
        return f'{WEEKDAYS[self.weekday - 1][1]}: {self.from_hour}—{self.to_hour}'

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
    type = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    worker = models.ForeignKey('Worker', on_delete=models.CASCADE)
    client = models.ForeignKey('Client', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.type} ({self.client})'


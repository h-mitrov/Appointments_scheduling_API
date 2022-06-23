from rest_framework import serializers

from .models import Location, Worker, Client, Schedule, Appointment


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('name',
                  'address',
                  'bookings'
                  )


class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = ('first_name',
                  'last_name',
                  'phone',
                  'specialty',
                  'work_schedule'
                  )


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('first_name',
                  'last_name',
                  'phone'
                  )


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ('__all__')


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ('type',
                  'start_time',
                  'end_time',
                  'worker',
                  'client'
                  )

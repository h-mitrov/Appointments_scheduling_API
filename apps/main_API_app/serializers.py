import json

from django.core.exceptions import ValidationError
from rest_framework import serializers
from django.contrib.auth.models import User, Permission
from django.db.models import ObjectDoesNotExist
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

from .models import Location, Worker, Client, Schedule, Appointment


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('pk',
                  'name',
                  'address',
                  'schedule_ids',
                  )

    def create(self, validated_data):
        try:
            location = Location(**validated_data)
            location.save()
            schedule_ids = [int(key) for key in json.loads(location.schedule_ids)]
            schedules = Schedule.objects.in_bulk(schedule_ids)

            for shed in schedules:
                location.work_schedule.add(shed)
        except ValidationError:
            raise serializers.ValidationError('Sorry, an error occured. Probably, because of schedule_ids wrong format.'
                                              'Try to pass a value like this — "[1,2,3]"')

        return location

    def update(self, instance, validated_data):
        previous_schedule = instance.schedule_ids

        instance.name = validated_data.get('name', instance.name)
        instance.address = validated_data.get('address', instance.address)
        instance.schedule_ids = validated_data.get('schedule_ids', instance.schedule_ids)

        if instance.schedule_ids != previous_schedule:
            try:
                schedule_ids = [int(key) for key in json.loads(instance.schedule_ids)]
                schedules = Schedule.objects.in_bulk(schedule_ids)

                for shed in schedules:
                    instance.work_schedule.add(shed)

            except ValidationError:
                raise serializers.ValidationError(
                    'Sorry, an error occured. Probably, because of schedule_ids wrong format.'
                    'Try to pass a value like this — "[1,2,3]"')
        instance.save()

        return instance

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'


class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = ('pk',
                  'first_name',
                  'last_name',
                  'phone',
                  'specialty',
                  'schedule_ids',
                  )

    def create(self, validated_data):
        try:
            worker = Worker(**validated_data)
            worker.save()
            schedule_ids = [int(key) for key in json.loads(worker.schedule_ids)]
            schedules = Schedule.objects.in_bulk(schedule_ids)

            for shed in schedules:
                worker.work_schedule.add(shed)
        except ValidationError:
            raise serializers.ValidationError('Sorry, an error occured. Probably, because of schedule_ids wrong format.'
                                              'Try to pass a value like this — "[1,2,3]"')

        return worker

    def update(self, instance, validated_data):
        previous_schedule = instance.schedule_ids

        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.specialty = validated_data.get('specialty', instance.specialty)
        instance.schedule_ids = validated_data.get('schedule_ids', instance.schedule_ids)

        if instance.schedule_ids != previous_schedule:
            try:
                schedule_ids = [int(key) for key in json.loads(instance.schedule_ids)]
                schedules = Schedule.objects.in_bulk(schedule_ids)

                for shed in schedules:
                    instance.work_schedule.add(shed)

            except ValidationError:
                raise serializers.ValidationError(
                    'Sorry, an error occured. Probably, because of schedule_ids wrong format.'
                    'Try to pass a value like this — "[1,2,3]"')
        instance.save()

        return instance


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('first_name',
                  'last_name',
                  'phone'
                  )


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ('type',
                  'date',
                  'start_time',
                  'end_time',
                  'worker',
                  'client',
                  'location'
                  )

    def create(self, validated_data):
        appointment = Appointment(
            type=validated_data['type'],
            date=validated_data['date'],
            start_time=validated_data['start_time'],
            end_time=validated_data['end_time'],
            worker=validated_data['worker'],
            client=validated_data['client'],
            location=validated_data['location']
        )

        try:
            appointment.clean()
            appointment.save()
        except ValidationError as argument:
            raise serializers.ValidationError(str(argument))

        return appointment


# New admin registration serializer
class RegisterAdminSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True,
                                   validators=[UniqueValidator(queryset=User.objects.all())]
                                   )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            is_staff=True
        )

        permissions = ['add_appointment',
                       'change_appointment',
                       'view_appointment',
                       'delete_appointment'
                       ]
        for text_perm in permissions:
            permission = Permission.objects.get(codename=text_perm)
            user.user_permissions.add(permission)

        user.save()
        return user

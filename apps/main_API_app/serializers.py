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

    def to_representation(self, instance):
        return {
            'pk': instance.pk,
            'weekday': instance.weekdays[instance.weekday - 1][1],
            'from_hour': instance.from_hour,
            'to_hour': instance.to_hour
        }

    def to_internal_value(self, data):
        weekdays = {
            'monday': 1,
            'tuesday': 2,
            'wednesday': 3,
            'thursday': 4,
            'friday': 5,
            'saturday': 6,
            'sunday': 7
        }
        weekday = weekdays.get(data.get('weekday').lower())
        from_hour = data.get('from_hour')
        to_hour = data.get('to_hour')

        return {
            'weekday': weekday,
            'from_hour': from_hour,
            'to_hour': to_hour
        }


class WorkerSerializer(serializers.ModelSerializer):
    work_schedule = ScheduleSerializer(many=True)

    class Meta:
        model = Worker
        fields = ('pk',
                  'first_name',
                  'last_name',
                  'phone',
                  'specialty',
                  # 'schedule_ids',
                  'work_schedule',
                  )

    def to_internal_value(self, data):
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        phone = data.get('phone')
        specialty = data.get('specialty')
        work_schedule = json.loads(data.get('work_schedule'))

        return {'first_name': first_name,
                'last_name': last_name,
                'phone': phone,
                'specialty': specialty,
                # 'schedule_ids': schedule_ids,
                'work_schedule': work_schedule
                }

    def create(self, validated_data):
        print('hello\n' * 100)
        try:
            schedules = validated_data.pop('work_schedule')
            worker = Worker(**validated_data)
            worker.save()

            weekdays = {
                'monday': 1,
                'tuesday': 2,
                'wednesday': 3,
                'thursday': 4,
                'friday': 5,
                'saturday': 6,
                'sunday': 7
            }

            if isinstance(schedules, dict):
                schedule_obj, created_status = Schedule.objects.get_or_create(
                    weekday=weekdays.get(schedules.get('weekday').lower()),
                    from_hour=schedules.get('from_hour'),
                    to_hour=schedules.get('to_hour'))

                worker.work_schedule.clear()
                worker.work_schedule.add(schedule_obj)

            elif isinstance(schedules, list):
                worker.work_schedule.clear()
                for sched in schedules:
                    schedule_obj, created_status = Schedule.objects.get_or_create(
                        weekday=weekdays.get(sched.get('weekday').lower()),
                        from_hour=sched.get('from_hour'),
                        to_hour=sched.get('to_hour'))
                    worker.work_schedule.add(schedule_obj)

        except ValidationError:
            raise serializers.ValidationError('Sorry, validation error occured.')

        return worker


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

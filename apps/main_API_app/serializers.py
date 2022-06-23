from rest_framework import serializers
from django.contrib.auth.models import User, Permission
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

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


# New admin registration serializers
class RegisterAdminSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
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

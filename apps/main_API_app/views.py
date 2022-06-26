from datetime import datetime, date

from django.contrib.auth.models import User
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.serializers import ValidationError

from .serializers import RegisterAdminSerializer, WorkerSerializer, AppointmentSerializer,\
    ClientSerializer, ScheduleSerializer, LocationSerializer
from .models import Worker, Appointment, Client, Schedule, Location
from .mixins import SuperuserRequiredMixin


# Basic views.
class WorkerViewSet(viewsets.ModelViewSet):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]


class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = [IsAuthenticated]


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]


# Manager's views
class RegisterAdminView(SuperuserRequiredMixin, generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterAdminSerializer
    permission_classes = [IsAuthenticated]


class RetrieveUpdateDeleteWorkerView(SuperuserRequiredMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WorkerSerializer
    queryset = Worker.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]


class RetrieveUpdateDeleteLocationView(SuperuserRequiredMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LocationSerializer
    queryset = Location.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]


# User's views
class FilterWorkersView(viewsets.ReadOnlyModelViewSet):
    serializer_class = WorkerSerializer

    def get_queryset(self):
        requested_date = self.request.query_params.get('date')
        current_date = datetime.today().date()
        if requested_date:
            try:
                requested_date = datetime.strptime(requested_date, '%Y-%m-%d').date()
                if requested_date < current_date:
                    raise ValidationError({'date': f'Date can not be in the past'})

            except ValueError:
                raise ValidationError({'date': f'time data {requested_date} does not match format %Y-%m-%d'})

        specialty = self.request.query_params.get('specialty')

        if requested_date and specialty:
            schedules = Schedule.objects.filter(weekday=requested_date.weekday() + 1)
            schedule_pks = [sched.pk for sched in schedules]
            queryset = Worker.objects.filter(specialty__iexact=specialty,
                                             work_schedule__in=schedule_pks)
        elif requested_date:
            schedules = Schedule.objects.filter(weekday=requested_date.weekday() + 1)
            schedule_pks = [sched.pk for sched in schedules]
            queryset = Worker.objects.filter(work_schedule__in=schedule_pks)

        elif specialty:
            queryset = Worker.objects.filter(specialty__iexact=specialty)

        else:
            queryset = Worker.objects.all()

        if not queryset:
            raise ValidationError('No results. Please, try to change the day and/or location query.')

        return queryset


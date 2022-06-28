# Standard library imports
from datetime import datetime

# Third party imports
from django.contrib.auth.models import User
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.serializers import ValidationError

# Local app imports
from .serializers import UserSerializer, WorkerSerializer, AppointmentSerializer,\
    ClientSerializer, ScheduleSerializer, LocationSerializer
from .models import Worker, Appointment, Client, Schedule, Location
from .mixins import SuperuserRequiredMixin


# Basic views
class WorkerViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Worker.
    """
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer
    permission_classes = [IsAuthenticated]


class AppointmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Appointment.
    """
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]


class ClientViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Client.
    """
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]


class ScheduleViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Schedule.
    """
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = [IsAuthenticated]


class LocationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Location.
    """
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ManagerViewSet(viewsets.ModelViewSet):
    """
    ViewSet for single User instance.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """
        Ensures, that all Users (Managers) list is available only to the superuser.
        """
        user = self.request.user
        if user.is_superuser:
            return User.objects.all()
        raise ValidationError({'no_rights': 'You have no permission to access this section. Only your manager can do that.'})


# Views for working with separate instances
class RetrieveUpdateDeleteWorkerView(SuperuserRequiredMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    ViewSet for single Worker instance.
    """
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer
    permission_classes = [IsAuthenticated]


class RetrieveUpdateDeleteLocationView(SuperuserRequiredMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    ViewSet for single Location instance.
    """
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticated]


class RetrieveUpdateDeleteAppointmentView(SuperuserRequiredMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    ViewSet for single Appointment instance.
    """
    queryset = Appointment.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticated]


class RetrieveUpdateDeleteManagerView(SuperuserRequiredMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    ViewSet for single User (Manager) instance.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Ensures, that all User (Manager) info is available only to the superuser.
        """
        user = self.request.user
        if user.is_superuser:
            return User.objects.all()
        return User.objects.filter(username=user.username)


# User's views
class FilterWorkersView(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for non-authenticated users. Allows retrieving and filtering Worker instances.
    """
    serializer_class = WorkerSerializer

    def get_serializer_context(self):
        """
        Allows passing url parameters from FilterWorkersView to serializer.
        """
        context = super(FilterWorkersView, self).get_serializer_context()
        context.update({'date': self.request.query_params.get('date')})
        return context

    def get_queryset(self):
        """
        Retrieves Worker database objects, that match search criteria by date and specialty.
        If not specified, retrieves all instances.
        """
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
            schedules = Schedule.objects.filter(weekday=requested_date.weekday())
            schedule_pks = [sched.pk for sched in schedules]
            queryset = Worker.objects.filter(specialty__iexact=specialty,
                                             work_schedule__in=schedule_pks)
        elif requested_date:
            schedules = Schedule.objects.filter(weekday=requested_date.weekday())
            schedule_pks = [sched.pk for sched in schedules]
            queryset = Worker.objects.filter(work_schedule__in=schedule_pks)

        elif specialty:
            queryset = Worker.objects.filter(specialty__iexact=specialty)

        else:
            queryset = Worker.objects.all()

        if not queryset:
            raise ValidationError({'date or specialty': 'No results. Please, try to change the day and/or specialty query.'})

        return queryset


from django.contrib.auth.models import User
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly


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

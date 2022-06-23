from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated


from .serializers import RegisterAdminSerializer, WorkerSerializer, AppointmentSerializer,\
    ClientSerializer, ScheduleSerializer, LocationSerializer
from .models import Worker, Appointment, Client, Schedule, Location
from .mixins import SuperuserRequiredMixin


# Basic views.
class WorkerViewSet(viewsets.ModelViewSet):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


# Manager's views
class RegisterAdminView(SuperuserRequiredMixin, generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterAdminSerializer

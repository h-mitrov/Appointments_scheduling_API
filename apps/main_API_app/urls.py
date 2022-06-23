from django.urls import include, path
from rest_framework import routers
from .views import WorkerViewSet, LocationViewSet, ScheduleViewSet, ClientViewSet, AppointmentViewSet

router = routers.DefaultRouter()
router.register(r'workers', WorkerViewSet)
router.register(r'clients', ClientViewSet)
router.register(r'locations', LocationViewSet)
router.register(r'appointments', AppointmentViewSet)
router.register(r'work_schedules', ScheduleViewSet)

urlpatterns = [
    path('', include(router.urls)),
]



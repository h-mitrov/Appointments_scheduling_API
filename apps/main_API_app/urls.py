from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import WorkerViewSet, LocationViewSet, ScheduleViewSet, ClientViewSet, AppointmentViewSet, RegisterAdminView,\
                   RetrieveUpdateDeleteWorkerView, RetrieveUpdateDeleteLocationView

router = routers.DefaultRouter()
router.register(r'workers', WorkerViewSet)
router.register(r'clients', ClientViewSet)
router.register(r'locations', LocationViewSet)
router.register(r'appointments', AppointmentViewSet)
router.register(r'work_schedules', ScheduleViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('workers/<int:pk>/', RetrieveUpdateDeleteWorkerView.as_view(), name='worker_get_delete_update'),
    path('locations/<int:pk>/', RetrieveUpdateDeleteLocationView.as_view(), name='location_get_delete_update'),
    path('auth/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register-admin/', RegisterAdminView.as_view(), name='admin_register'),
]

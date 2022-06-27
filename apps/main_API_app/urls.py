from django.urls import include, path, re_path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import WorkerViewSet, LocationViewSet, ScheduleViewSet, ClientViewSet, AppointmentViewSet, ManagerViewSet, \
    RetrieveUpdateDeleteWorkerView, RetrieveUpdateDeleteLocationView, FilterWorkersView, \
    RetrieveUpdateDeleteManagerView, RetrieveUpdateDeleteAppointmentView

router = routers.DefaultRouter()
router.register(r'workers', WorkerViewSet)
router.register(r'managers', ManagerViewSet)
router.register(r'clients', ClientViewSet)
router.register(r'locations', LocationViewSet)
router.register(r'appointments', AppointmentViewSet)
router.register(r'work_schedules', ScheduleViewSet)
router.register(r'filter-specialists', FilterWorkersView, basename='Worker')

urlpatterns = [
    path('', include(router.urls)),
    path('managers/<int:id>/', RetrieveUpdateDeleteManagerView.as_view(), name='manager_get_delete_update'),
    path('workers/<int:pk>/', RetrieveUpdateDeleteWorkerView.as_view(), name='worker_get_delete_update'),
    path('locations/<int:pk>/', RetrieveUpdateDeleteLocationView.as_view(), name='location_get_delete_update'),
    path('appointments/<int:pk>/', RetrieveUpdateDeleteAppointmentView.as_view(), name='appointment_get_delete_update'),
    re_path(r'^filter-specialists/(?P<date>)/(?P<specialty>\w+)$', FilterWorkersView.as_view({'get': 'list'}), name='filter_workers'),
    path('auth/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

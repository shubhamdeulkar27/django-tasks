from django.urls import include, path
from .views import TaskViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
    path('', include(router.urls)),
]
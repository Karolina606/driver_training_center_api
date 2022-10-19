"""driver_training_center_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import accounts.urls
from django.contrib import admin

from django.urls import include, path
from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view

from driver_training_center_db.views import *
from accounts.views import *


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'permissions', PermissionViewSet)
router.register(r'driving_license_categories', DrivingLicenseCategoryViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'lessons', LessonViewSet)
router.register(r'student_course_status', CourseStatusViewSet, basename="coursestatus")

schema_view = get_swagger_view(title='Driver training center API')

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
    path('swagger', schema_view),
    path('accounts/', include('accounts.urls'))
]
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path('', include('read_app.urls')),
    path('assessment/', include('assessment.urls')),
    path('materials/', include('materials.urls')),
    path('students/', include('students.urls')),
    path('admin/', admin.site.urls),
] 

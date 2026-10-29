"""
URL configuration for webgis project.

admin/ goes to the Django admin, everything else to the districts app.
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("districts.urls")),
]

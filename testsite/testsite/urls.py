from django.contrib import admin
from django.urls import include, path

from testapp import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("aceshigh/", include("aceshigh.urls")),
    path("api/", include("aceshigh.api_urls")),
    path("", views.home),
]

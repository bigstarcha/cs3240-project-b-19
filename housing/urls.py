from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("accounts/", include("allauth.urls")),
    path("logout/", LogoutView.as_view(), name="logout"),
]

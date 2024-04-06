from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("secret/", admin.site.urls),
    path("admin/", include("admin_honeypot.urls", namespace="admin_honeypot")),
    path("", include("core.urls")),
    path("accounts/", include("allauth.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


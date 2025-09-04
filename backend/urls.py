from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("core.urls")),
    # 👇 Root route (homepage)
    path("", lambda request: HttpResponse("✅ Backend is running on Render!")),
]

# Serve media files in DEBUG mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from core import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),
    # path('api/login/', views.admin_login),
    # path('api/admins/', views.get_admins),
    
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

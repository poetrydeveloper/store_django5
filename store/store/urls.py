# this  main app project store\urls
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('goods.urls')),  # Изменил путь с api/goods/ на api/
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
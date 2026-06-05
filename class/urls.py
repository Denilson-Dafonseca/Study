from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from lesson import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('lesson.urls')),  # This includes all core URLs
    path('accounts/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


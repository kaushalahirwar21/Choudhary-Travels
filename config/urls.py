"""
URL configuration for Choudhary Travels project.
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from booking import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('secure-login/', RedirectView.as_view(url='/admin/', permanent=False)),
    path('', include('booking.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
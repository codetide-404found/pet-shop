from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from pets import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name="home"),  # home page from pets app
    path("", include("pets.urls")),
  # include all pets routes
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = "PlacePro Administration"
admin.site.site_title = "PlacePro Admin"
admin.site.index_title = "Manage Placement Portal"

handler404 = 'portal.views.custom_404'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('portal.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('grappelli/', include('grappelli.urls')),
    path('admin/', admin.site.urls),
    path('', include('ads.urls')),
    path('ads/', include('ads.urls')),
    path('account/', include('account.urls')),
    path('chat/', include('chat.urls')),
    path('info/', include('info.urls')),
    path('api/v1/', include('ads.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

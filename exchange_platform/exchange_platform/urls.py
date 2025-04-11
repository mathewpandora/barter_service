from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ads.urls')),
    path('ads/', include('ads.urls')),
    path('account/', include('account.urls')),
    path('chat/', include('chat.urls')),

]


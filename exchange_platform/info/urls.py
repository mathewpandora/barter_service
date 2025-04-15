from django.urls import path
from .views import info_page

urlpatterns = [
    path('info/', info_page, name='info_page'),  # Явно указываем путь
]


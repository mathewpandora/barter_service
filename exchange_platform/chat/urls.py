from django.urls import path
from . import views

urlpatterns = [
    path('chat/<int:proposal_id>/', views.chat_view, name='chat_view'),
path('list/', views.chat_list_view, name='chat_list'),
]
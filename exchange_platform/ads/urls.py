from rest_framework.authtoken.views import obtain_auth_token
from .views import UserRegistrationView, AdListCreateView, AdDetailView
from django.urls import path
from . import views

urlpatterns = [
    path('', views.redirect_view, name='redirect'),
    path('create/', views.create_ad, name='create_ad'),
    path('edit/<int:ad_id>/', views.edit_ad, name='edit_ad'),
    path('delete/<int:ad_id>/', views.delete_ad, name='delete_ad'),
    path('list/', views.ad_list, name='ad_list'),
    path('<int:ad_id>/', views.ad_detail, name='ad_detail'),
    path('my/', views.my_ads, name='my_ads'),
    path('my-barters/', views.my_barters, name='my_barters'),
    path('propose-exchange/<int:ad_id>/', views.propose_exchange, name='propose_exchange'),
    path('accept/<int:proposal_id>/', views.accept_exchange, name='accept_exchange'),
    path('decline/<int:proposal_id>/', views.decline_exchange, name='decline_exchange'),
    path('login/', obtain_auth_token, name='api_token_auth'),
    path('register/', UserRegistrationView.as_view(), name='api_register'),
    path('ads/', AdListCreateView.as_view(), name='ad-list-create'),
    path('ads/<int:ad_id>/', AdDetailView.as_view(), name='ad-detail'),

]

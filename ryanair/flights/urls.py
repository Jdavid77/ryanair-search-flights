"""
URL configuration for the flights app.
"""
from django.urls import path
from . import views

app_name = 'flights'

urlpatterns = [
    # Main search page
    path('', views.search_view, name='search'),
    
    # API endpoints
    path('api/search/', views.search_flights_api, name='search_api'),
    path('api/destinations/<str:departure_airport>/', views.get_destinations_api, name='destinations_api'),
]
from django.urls import path, include
from . import views

urlpatterns = [
    path('edit/', views.edit_profile, name='profile.edit'),
]
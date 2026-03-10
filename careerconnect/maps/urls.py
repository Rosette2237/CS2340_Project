from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='maps.index'),
    path('recruiter/', views.recruiter_map, name='maps.recruiter'),
]
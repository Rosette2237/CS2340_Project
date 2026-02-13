from django.urls import path, include
from . import views

urlpatterns = [
    path('edit/', views.edit_profile, name='profile.edit'),
    path('signup/', views.signup, name='accounts.signup'),
    path('login/', views.login, name='accounts.login'),
    path('logout/', views.logout, name='accounts.logout'),

]
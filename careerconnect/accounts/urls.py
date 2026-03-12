from django.urls import path, include
from . import views

urlpatterns = [
    path('edit/', views.edit_profile, name='profile.edit'),
    path('signup/', views.signup, name='accounts.signup'),
    path('login/', views.login, name='accounts.login'),
    path('logout/', views.logout, name='accounts.logout'),
    path('search/', views.search_candidates, name='accounts.search'),
    path('search/save/', views.save_search, name='save_search'),
    path('my-searches/', views.search_list, name='my_searches'),
    path('searches/<int:search_id>/delete/', views.delete_search, name='delete_search'),
    path('searches/<int:search_id>/toggle/', views.applied_search, name='applied_search'),
]

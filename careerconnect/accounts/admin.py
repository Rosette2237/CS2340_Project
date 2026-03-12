# accounts/admin.py

import csv
from django.http import HttpResponse
from django.contrib import admin
from .models import Profile, SavedSearch


@admin.action(description="Export selected profiles as CSV")
def export_profiles_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users_export.csv"'
    writer = csv.writer(response)
    writer.writerow([
        'User ID', 'Username', 'Email', 'Role',
        'City', 'State', 'Skills', 'Headline',
        'Public Profile', 'Date Joined',
        'Total Time On Site (seconds)', 'Total Time On Site (formatted)',  
        'Last Activity',                                                   
    ])
    for profile in queryset.select_related('user'):
        writer.writerow([
            profile.user.id,
            profile.user.username,
            profile.user.email,
            'Recruiter' if profile.is_recruiter else 'Candidate',
            profile.city,
            profile.state,
            profile.skills,
            profile.headline,
            'Yes' if profile.is_public else 'No',
            profile.user.date_joined.strftime('%Y-%m-%d'),
            round(profile.total_time_on_site),                          
            profile.formatted_time_on_site,                              
            profile.last_activity.strftime('%Y-%m-%d %H:%M') if profile.last_activity else 'Never', 
        ])
    return response


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    actions       = [export_profiles_csv]
    list_display  = ['user', 'is_recruiter', 'city', 'state', 'is_public',
                     'formatted_time_on_site', 'last_activity']            
    list_filter   = ['is_recruiter', 'is_public']
    search_fields = ['user__username', 'skills', 'city']


@admin.action(description="Export selected saved searches as CSV")
def export_saved_searches_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="saved_searches_export.csv"'
    writer = csv.writer(response)
    writer.writerow([
        'ID', 'Recruiter Username', 'Recruiter Email',
        'Skills Filter', 'City Filter', 'State Filter',
        'Notifications Active', 'Created At',
    ])
    for s in queryset.select_related('recruiter').order_by('-creation_date'):
        writer.writerow([
            s.id,
            s.recruiter.username,
            s.recruiter.email,
            s.skills,
            s.city,
            s.state,
            'Yes' if s.is_applicable else 'No',
            s.creation_date.strftime('%Y-%m-%d %H:%M'),
        ])
    return response


@admin.register(SavedSearch)
class SavedSearchAdmin(admin.ModelAdmin):
    actions       = [export_saved_searches_csv]
    list_display  = ['id', 'recruiter', 'skills', 'city', 'state', 'is_applicable', 'creation_date']
    list_filter   = ['is_applicable']
    search_fields = ['recruiter__username', 'skills', 'city']
    ordering      = ['-creation_date']
import csv
from django.http import HttpResponse
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import User, Group


@admin.action(description="Export selected users as CSV")
def export_users_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users_export.csv"'
    writer = csv.writer(response)
    writer.writerow([
        'ID', 'Username', 'Email', 'First Name', 'Last Name',
        'Staff', 'Superuser', 'Active', 'Date Joined', 'Last Login',
    ])
    for user in queryset.order_by('date_joined'):
        writer.writerow([
            user.id,
            user.username,
            user.email,
            user.first_name,
            user.last_name,
            'Yes' if user.is_staff else 'No',
            'Yes' if user.is_superuser else 'No',
            'Yes' if user.is_active else 'No',
            user.date_joined.strftime('%Y-%m-%d %H:%M'),
            user.last_login.strftime('%Y-%m-%d %H:%M') if user.last_login else 'Never',
        ])
    return response

admin.site.unregister(User)

@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    actions = list(BaseUserAdmin.actions or []) + [export_users_csv]


@admin.action(description="Export selected groups as CSV")
def export_groups_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="groups_export.csv"'
    writer = csv.writer(response)
    writer.writerow(['ID', 'Group Name', 'Permissions Count', 'Member Count'])
    for group in queryset.prefetch_related('permissions', 'user_set'):
        writer.writerow([
            group.id,
            group.name,
            group.permissions.count(),
            group.user_set.count(),
        ])
    return response

admin.site.unregister(Group)

@admin.register(Group)
class CustomGroupAdmin(BaseGroupAdmin):
    actions = list(BaseGroupAdmin.actions or []) + [export_groups_csv]
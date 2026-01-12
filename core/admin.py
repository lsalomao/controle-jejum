from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, FastingRecord, WeightRecord


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'name', 'fasting_goal_hours', 'is_active', 'created_at']
    list_filter = ['is_active', 'is_staff', 'created_at']
    search_fields = ['email', 'name']
    ordering = ['-created_at']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informações Pessoais', {'fields': ('name', 'fasting_goal_hours')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas Importantes', {'fields': ('last_login', 'created_at')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2', 'fasting_goal_hours', 'is_active', 'is_staff'),
        }),
    )

    readonly_fields = ['created_at', 'last_login']


@admin.register(FastingRecord)
class FastingRecordAdmin(admin.ModelAdmin):
    list_display = ['user', 'start_time', 'end_time', 'duration_hours', 'fasting_type', 'created_at']
    list_filter = ['fasting_type', 'created_at', 'user']
    search_fields = ['user__email', 'user__name', 'notes']
    ordering = ['-start_time']
    readonly_fields = ['duration_hours', 'created_at']

    fieldsets = (
        ('Usuário', {'fields': ('user',)}),
        ('Período', {'fields': ('start_time', 'end_time', 'duration_hours')}),
        ('Detalhes', {'fields': ('fasting_type', 'energy_level', 'focus_level', 'mood_level', 'notes')}),
        ('Metadados', {'fields': ('created_at',)}),
    )


@admin.register(WeightRecord)
class WeightRecordAdmin(admin.ModelAdmin):
    list_display = ['user', 'weight', 'reference_month', 'created_at']
    list_filter = ['reference_month', 'created_at', 'user']
    search_fields = ['user__email', 'user__name']
    ordering = ['-reference_month']
    readonly_fields = ['created_at']

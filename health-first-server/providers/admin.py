"""
Django admin configuration for providers app.
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import Provider, ClinicAddress, ProviderRegistrationLog


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    """Admin interface for Provider model."""
    
    list_display = (
        'email', 'first_name', 'last_name', 'specialization',
        'verification_status', 'email_verified', 'is_active', 'created_at'
    )
    
    list_filter = (
        'verification_status', 'email_verified', 'is_active',
        'specialization', 'created_at', 'updated_at'
    )
    
    search_fields = (
        'email', 'first_name', 'last_name', 'license_number',
        'phone_number'
    )
    
    readonly_fields = (
        'id', 'password', 'created_at', 'updated_at',
        'email_verification_token', 'email_verification_expires'
    )
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone_number')
        }),
        ('Professional Information', {
            'fields': ('specialization', 'license_number', 'years_of_experience')
        }),
        ('Account Status', {
            'fields': (
                'verification_status', 'email_verified', 'is_active',
                'email_verification_token', 'email_verification_expires'
            )
        }),
        ('Permissions', {
            'fields': ('is_staff', 'is_superuser'),
            'classes': ('collapse',)
        }),
        ('Important Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
        ('System Information', {
            'fields': ('id', 'password'),
            'classes': ('collapse',)
        })
    )
    
    ordering = ('-created_at',)
    
    def has_add_permission(self, request):
        """Disable adding providers through admin."""
        return False
    
    def verification_status_display(self, obj):
        """Display verification status with colored badge."""
        colors = {
            'pending': 'orange',
            'verified': 'green',
            'rejected': 'red'
        }
        color = colors.get(obj.verification_status, 'gray')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_verification_status_display()
        )
    verification_status_display.short_description = 'Verification Status'
    
    def email_verified_display(self, obj):
        """Display email verification status."""
        if obj.email_verified:
            return format_html('<span style="color: green;">✓ Verified</span>')
        else:
            return format_html('<span style="color: red;">✗ Not Verified</span>')
    email_verified_display.short_description = 'Email Verified'
    
    actions = ['verify_provider', 'reject_provider', 'activate_provider', 'deactivate_provider']
    
    def verify_provider(self, request, queryset):
        """Bulk action to verify providers."""
        updated = queryset.update(verification_status='verified')
        self.message_user(request, f'{updated} providers were verified.')
    verify_provider.short_description = 'Verify selected providers'
    
    def reject_provider(self, request, queryset):
        """Bulk action to reject providers."""
        updated = queryset.update(verification_status='rejected')
        self.message_user(request, f'{updated} providers were rejected.')
    reject_provider.short_description = 'Reject selected providers'
    
    def activate_provider(self, request, queryset):
        """Bulk action to activate providers."""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} providers were activated.')
    activate_provider.short_description = 'Activate selected providers'
    
    def deactivate_provider(self, request, queryset):
        """Bulk action to deactivate providers."""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} providers were deactivated.')
    deactivate_provider.short_description = 'Deactivate selected providers'


@admin.register(ClinicAddress)
class ClinicAddressAdmin(admin.ModelAdmin):
    """Admin interface for ClinicAddress model."""
    
    list_display = ('street', 'city', 'state', 'zip_code', 'provider_name')
    list_filter = ('state', 'city')
    search_fields = ('street', 'city', 'state', 'zip_code', 'provider__email')
    
    def provider_name(self, obj):
        """Display provider name."""
        if hasattr(obj, 'provider'):
            return obj.provider.get_full_name()
        return 'No Provider'
    provider_name.short_description = 'Provider'


@admin.register(ProviderRegistrationLog)
class ProviderRegistrationLogAdmin(admin.ModelAdmin):
    """Admin interface for ProviderRegistrationLog model."""
    
    list_display = (
        'email', 'ip_address', 'success', 'created_at'
    )
    
    list_filter = ('success', 'created_at')
    search_fields = ('email', 'ip_address', 'error_message')
    readonly_fields = ('ip_address', 'email', 'success', 'error_message', 'user_agent', 'created_at')
    
    def has_add_permission(self, request):
        """Disable adding logs through admin."""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Disable editing logs."""
        return False
    
    def has_delete_permission(self, request, obj=None):
        """Allow deleting old logs."""
        return request.user.is_superuser 
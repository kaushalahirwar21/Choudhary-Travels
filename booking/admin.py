from django.contrib import admin

from .models import Booking, ContactMessage, Service, Testimonial, Vehicle

admin.site.site_header = 'Choudhary Travels Admin'
admin.site.site_title = 'Choudhary Travels'
admin.site.index_title = 'Manage Bookings & Fleet'
admin.site.site_url = '/'


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'seats', 'price_per_km', 'price_per_day', 'is_available', 'is_featured', 'edit_link')
    list_filter = ('category', 'is_available', 'is_featured')
    search_fields = ('name', 'description')
    list_editable = ('is_available', 'is_featured')
    actions = ['make_featured', 'make_unfeatured', 'make_available', 'make_unavailable']

    @admin.action(description='Mark selected vehicles as Featured ⭐️')
    def make_featured(self, request, queryset):
        queryset.update(is_featured=True)

    @admin.action(description='Mark selected vehicles as Not Featured ❌')
    def make_unfeatured(self, request, queryset):
        queryset.update(is_featured=False)

    @admin.action(description='Mark selected vehicles as Available ✅')
    def make_available(self, request, queryset):
        queryset.update(is_available=True)

    @admin.action(description='Mark selected vehicles as Unavailable ❌')
    def make_unavailable(self, request, queryset):
        queryset.update(is_available=False)

    def edit_link(self, obj):
        from django.urls import reverse
        from django.utils.html import format_html
        url = reverse('admin:booking_vehicle_change', args=[obj.pk])
        return format_html('<a href="{}" style="padding: 4px 8px; background: #3b82f6; color: white; border-radius: 4px; text-decoration: none; font-weight: bold; font-size: 0.8rem;">Edit 📝</a>', url)
    edit_link.short_description = 'Edit'


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'customer_name', 'phone', 'pickup_location', 'drop_location',
        'pickup_date', 'vehicle', 'status', 'whatsapp_sent', 'created_at', 'edit_link'
    )
    list_filter = ('status', 'trip_type', 'whatsapp_sent', 'pickup_date')
    search_fields = ('customer_name', 'phone', 'email', 'pickup_location', 'drop_location')
    readonly_fields = ('created_at', 'updated_at', 'whatsapp_sent')
    date_hierarchy = 'pickup_date'
    actions = ['confirm_bookings', 'cancel_bookings']

    @admin.action(description='Confirm selected bookings ✅')
    def confirm_bookings(self, request, queryset):
        queryset.update(status='confirmed')

    @admin.action(description='Cancel selected bookings ❌')
    def cancel_bookings(self, request, queryset):
        queryset.update(status='cancelled')

    def edit_link(self, obj):
        from django.urls import reverse
        from django.utils.html import format_html
        url = reverse('admin:booking_booking_change', args=[obj.pk])
        return format_html('<a href="{}" style="padding: 4px 8px; background: #3b82f6; color: white; border-radius: 4px; text-decoration: none; font-weight: bold; font-size: 0.8rem;">Edit 📝</a>', url)
    edit_link.short_description = 'Edit'

    fieldsets = (
        ('Customer', {
            'fields': ('customer_name', 'phone', 'email', 'passengers'),
        }),
        ('Trip Details', {
            'fields': (
                'trip_type', 'pickup_location', 'drop_location',
                'pickup_date', 'return_date', 'pickup_time', 'vehicle', 'message',
            ),
        }),
        ('Status', {
            'fields': ('status', 'admin_notes', 'whatsapp_sent', 'created_at', 'updated_at'),
        }),
    )


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'is_read', 'created_at')
    list_filter = ('is_read',)
    search_fields = ('name', 'email', 'subject', 'message')
    list_editable = ('is_read',)
    readonly_fields = ('created_at',)


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'location', 'rating', 'is_active', 'created_at')
    list_filter = ('is_active', 'rating')
    list_editable = ('is_active',)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon', 'sort_order', 'is_active')
    list_editable = ('sort_order', 'is_active')
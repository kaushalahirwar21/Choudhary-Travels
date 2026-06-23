from django.contrib import admin

from .models import Booking, ContactMessage, Service, Testimonial, Vehicle

admin.site.site_header = 'Choudhary Travels Admin'
admin.site.site_title = 'Choudhary Travels'
admin.site.index_title = 'Manage Bookings & Fleet'
admin.site.site_url = '/'


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'seats', 'price_per_km', 'price_per_day', 'is_available', 'is_featured')
    list_filter = ('category', 'is_available', 'is_featured')
    search_fields = ('name', 'description')
    list_editable = ('is_available', 'is_featured')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'customer_name', 'phone', 'pickup_location', 'drop_location',
        'pickup_date', 'vehicle', 'status', 'whatsapp_sent', 'created_at',
    )
    list_filter = ('status', 'trip_type', 'whatsapp_sent', 'pickup_date')
    search_fields = ('customer_name', 'phone', 'email', 'pickup_location', 'drop_location')
    readonly_fields = ('created_at', 'updated_at', 'whatsapp_sent')
    date_hierarchy = 'pickup_date'
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
from django.contrib import admin
from .models import WasteCategory, WasteReport, UserProfile, UserPoints, PointsTransaction, Coupon, UserCoupon

@admin.register(WasteCategory)
class WasteCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'icon')
    search_fields = ('name', 'description')
    list_filter = ('name',)

@admin.register(WasteReport)
class WasteReportAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'quantity', 'date', 'location')
    search_fields = ('user__username', 'category__name', 'location')
    list_filter = ('category', 'date')
    readonly_fields = ('date',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'total_waste_recorded')
    search_fields = ('user__username', 'location')
    readonly_fields = ('total_waste_recorded',)

@admin.register(UserPoints)
class UserPointsAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_points', 'redeemed_points', 'available_points')
    search_fields = ('user__username',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(PointsTransaction)
class PointsTransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'points', 'transaction_type', 'description', 'created_at')
    search_fields = ('user__username', 'description')
    list_filter = ('transaction_type', 'created_at')
    readonly_fields = ('created_at',)

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('coupon_code', 'name', 'points_required', 'discount_percentage', 'active', 'current_uses')
    search_fields = ('coupon_code', 'name')
    list_filter = ('active', 'created_at')
    readonly_fields = ('current_uses', 'created_at', 'valid_from')
    fieldsets = (
        ('Coupon Info', {
            'fields': ('name', 'coupon_code', 'description', 'icon', 'color')
        }),
        ('Points & Discount', {
            'fields': ('points_required', 'discount_percentage', 'discount_amount')
        }),
        ('Availability', {
            'fields': ('active', 'max_uses', 'current_uses', 'valid_from', 'valid_until')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

@admin.register(UserCoupon)
class UserCouponAdmin(admin.ModelAdmin):
    list_display = ('user', 'coupon', 'quantity', 'first_redeemed_at', 'last_updated')
    search_fields = ('user__username', 'coupon__coupon_code')
    list_filter = ('first_redeemed_at', 'last_updated')
    readonly_fields = ('first_redeemed_at', 'last_updated')
    fieldsets = (
        ('Coupon Assignment', {
            'fields': ('user', 'coupon', 'quantity')
        }),
        ('Timestamps', {
            'fields': ('first_redeemed_at', 'last_updated'),
            'classes': ('collapse',)
        }),
    )

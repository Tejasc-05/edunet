from django.contrib import admin
from .models import WasteCategory, WasteReport, UserProfile

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

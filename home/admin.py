# admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import *

class PortfolioImageInline(admin.TabularInline):
    model = PortfolioImage
    extra = 1
    fields = ['image', 'caption', 'alt_text', 'display_order', 'is_primary']
    readonly_fields = ['image_preview']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="100" height="100" style="object-fit: cover;" />',
                obj.image.url
            )
        return "-"
    image_preview.short_description = "Preview"

class PortfolioVideoInline(admin.TabularInline):
    model = PortfolioVideo
    extra = 1
    fields = ['video_type', 'video_file', 'video_url', 'title', 'display_order']

class PortfolioCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

@admin.register(PortfolioItem)
class PortfolioItemAdmin(admin.ModelAdmin):
    list_display = [
        'title', 
        'project_type', 
        'category', 
        'status', 
        'is_featured', 
        'display_order',
        'created_at'
    ]
    list_filter = ['project_type', 'status', 'category', 'is_featured', 'created_at']
    search_fields = ['title', 'description', 'client_name']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at']
    inlines = [PortfolioImageInline, PortfolioVideoInline]
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'title', 'slug', 'description', 'short_description',
                'featured_image', 'is_featured', 'display_order'
            )
        }),
        ('Categorization', {
            'fields': ('category', 'project_type', 'status')
        }),
        ('Project Details', {
            'fields': (
                'client_name', 'location', 'project_date', 
                'completion_date', 'budget'
            )
        }),
        ('System Information', {
            'fields': ('created_by', 'is_active', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


class PortfolioImageAdmin(admin.ModelAdmin):
    list_display = ['portfolio_item', 'caption', 'display_order', 'is_primary', 'uploaded_at']
    list_filter = ['portfolio_item', 'is_primary']
    readonly_fields = ['image_preview']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="200" height="200" style="object-fit: cover;" />',
                obj.image.url
            )
        return "-"
    image_preview.short_description = "Preview"


class PortfolioVideoAdmin(admin.ModelAdmin):
    list_display = ['portfolio_item', 'video_type', 'title', 'display_order']
    list_filter = ['video_type', 'portfolio_item']







class TestimonialInline(admin.TabularInline):
    model = Testimonial
    extra = 1

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'active')
    inlines = [TestimonialInline]

class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'client', 'display', 'created_at')
    list_filter = ('display', 'client')
    search_fields = ('author_name', 'quote')


class SocialLinkInline(admin.TabularInline):
    model = SocialLink
    extra = 1

@admin.register(BasicWebsiteInfo)
class BasicWebsiteInfoAdmin(admin.ModelAdmin):
    inlines = [SocialLinkInline]
    def has_add_permission(self, request):
        # Allow adding only if no instance exists
        if BasicWebsiteInfo.objects.exists():
            return False
        return True


class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ('platform', 'url')
    list_filter = ('platform',)
    search_fields = ('url',)





@admin.register(IndustrialPage)
class IndustrialPageAdmin(admin.ModelAdmin):
    list_display = ("hero_title", "is_active", "updated_at")
    list_editable = ("is_active",)
    search_fields = ("hero_title",)
    readonly_fields = ("updated_at",)

@admin.register(ImportExportProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    search_fields = ('title', 'description')


@admin.register(HeroMedia)
class HeroMediaAdmin(admin.ModelAdmin):
    # Organize fields into visually distinct, collapsible groups
    fieldsets = (
        (" Landing Page", {
            'fields': ('landing_background_image', 'landing_background_video'),
            'classes': ('collapse',),
            'description': "Upload the background image or video for the landing page."
        }),
        (" Construction Page", {
            'fields': ('construction_background_image', 'construction_background_video'),
            'classes': ('collapse',),
            'description': "Upload hero section media for the construction page."
        }),
        (" Industrial Page", {
            'fields': ('industrial_background_image', 'industrial_background_video'),
            'classes': ('collapse',),
            'description': "Upload hero section media for the industrial page."
        }),
        (" Import & Export Page", {
            'fields': ('import_export_background_image', 'import_export_background_video'),
            'classes': ('collapse',),
            'description': "Upload hero section media for the import/export page."
        }),
        (" Transport Page", {
            'fields': ('transport_background_image', 'transport_background_video'),
            'classes': ('collapse',),
            'description': "Upload hero section media for the transport page."
        }),
        (" Meta Info", {
            'fields': ('updated_at',),
        }),
    )

    readonly_fields = ('updated_at',)
    list_display = ('__str__', 'updated_at')
    ordering = ('-updated_at',)

    # Disable adding multiple instances
    def has_add_permission(self, request):
        """Allow adding only one instance."""
        return not HeroMedia.objects.exists()

    def has_delete_permission(self, request, obj=None):
        """Optional: prevent accidental deletion."""
        return False
    
class VehicleFeatureInline(admin.TabularInline):
    model = VehicleFeature
    extra = 1


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    ordering = ('order',)
    inlines = [VehicleFeatureInline]
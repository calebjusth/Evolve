# models.py
from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
from django.utils import timezone
import os
import uuid
from django.utils.text import slugify

def portfolio_image_path(instance, filename):
    """Generate file path for portfolio images"""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('portfolio/images/', filename)

def portfolio_video_path(instance, filename):
    """Generate file path for portfolio videos"""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('portfolio/videos/', filename)

class PortfolioCategory(models.Model):
    """Category model for organizing portfolio items"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, db_index=True)  # Added index
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)  # Added index
    
    class Meta:
        verbose_name_plural = "Portfolio Categories"
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),  # Added for name searches
        ]
    
    def __str__(self):
        return self.name

class PortfolioItem(models.Model):
    """Main portfolio item model"""
    
    PROJECT_TYPE_CHOICES = [
        ('construction', 'Construction'),
        ('industrial', 'Industrial'),
        ('transportation', 'Transportation'),
        ('import_export', 'Import & Export'),
    ]
    
    STATUS_CHOICES = [
        ('completed', 'Completed'),
        ('in_progress', 'In Progress'),
        ('planned', 'Planned'),
    ]
    
    # Basic Information
    title = models.CharField(max_length=200, db_index=True)  # Added index
    slug = models.SlugField(max_length=200, unique=True, db_index=True)  # Added index
    description = models.TextField()
    short_description = models.CharField(max_length=300, blank=True)
    
    # Categorization
    category = models.ForeignKey(
        PortfolioCategory, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='portfolio_items',
        db_index=True  # Added index
    )
    project_type = models.CharField(
        max_length=20, 
        choices=PROJECT_TYPE_CHOICES, 
        default='construction',
        db_index=True  # Added index
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='completed',
        db_index=True  # Added index
    )
    
    # Project Details
    client_name = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=200, blank=True)
    project_date = models.DateField(default=timezone.now, db_index=True)  # Added index
    completion_date = models.DateField(null=True, blank=True)
    budget = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        null=True, 
        blank=True
    )
    
    # Technical Details
    featured_image = models.ImageField(
        upload_to=portfolio_image_path,
        null=True,
        blank=True
    )
    is_featured = models.BooleanField(default=False, db_index=True)  # Added index
    display_order = models.PositiveIntegerField(default=0)
    
    # Meta Information
    created_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='portfolio_items',
        db_index=True  # Added index
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)  # Added index
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, db_index=True)  # Added index
    
    
    class Meta:
        ordering = ['display_order', '-created_at']
        verbose_name_plural = "Portfolio Items"
        indexes = [
            models.Index(fields=['project_type', 'status']),
            models.Index(fields=['is_featured', 'is_active']),
            models.Index(fields=['created_at']),
            # Composite indexes for common queries
            models.Index(fields=['project_type', 'is_active', 'is_featured']),
            models.Index(fields=['project_type', 'is_active', 'created_at']),
            models.Index(fields=['is_active', 'is_featured', 'created_at']),
        ]
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    @property
    def duration(self):
        """Calculate project duration"""
        if self.completion_date and self.project_date:
            return (self.completion_date - self.project_date).days
        return None
    
    @property
    def primary_image(self):
        """Get primary image for display"""
        if self.featured_image:
            return self.featured_image
        first_image = self.images.first()
        return first_image.image if first_image else None

class PortfolioImage(models.Model):
    """Multiple images for a portfolio item"""
    portfolio_item = models.ForeignKey(
        PortfolioItem,
        on_delete=models.CASCADE,
        related_name='images',
        db_index=True  # Added index
    )
    image = models.ImageField(upload_to=portfolio_image_path)
    caption = models.CharField(max_length=200, blank=True)
    alt_text = models.CharField(max_length=200, blank=True)
    display_order = models.PositiveIntegerField(default=0)
    is_primary = models.BooleanField(default=False, db_index=True)  # Added index
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['display_order', 'uploaded_at']
        verbose_name_plural = "Portfolio Images"
        indexes = [
            models.Index(fields=['portfolio_item', 'is_primary']),
            models.Index(fields=['portfolio_item', 'display_order']),
        ]
    
    def __str__(self):
        return f"Image for {self.portfolio_item.title}"
    
    def save(self, *args, **kwargs):
        if self.is_primary:
            # Ensure only one primary image per portfolio item
            PortfolioImage.objects.filter(
                portfolio_item=self.portfolio_item, 
                is_primary=True
            ).update(is_primary=False)
        super().save(*args, **kwargs)

class PortfolioVideo(models.Model):
    """Multiple videos for a portfolio item"""
    
    VIDEO_TYPE_CHOICES = [
        ('upload', 'Uploaded Video'),
        ('youtube', 'YouTube'),
        ('vimeo', 'Vimeo'),
    ]
    
    portfolio_item = models.ForeignKey(
        PortfolioItem,
        on_delete=models.CASCADE,
        related_name='videos',
        db_index=True  # Added index
    )
    video_type = models.CharField(
        max_length=10, 
        choices=VIDEO_TYPE_CHOICES, 
        default='upload'
    )
    video_file = models.FileField(
        upload_to=portfolio_video_path,
        null=True,
        blank=True
    )
    video_url = models.URLField(blank=True)  # For YouTube/Vimeo links
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    thumbnail = models.ImageField(
        upload_to=portfolio_image_path,
        null=True,
        blank=True
    )
    display_order = models.PositiveIntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['display_order', 'uploaded_at']
        verbose_name_plural = "Portfolio Videos"
        indexes = [
            models.Index(fields=['portfolio_item', 'display_order']),
        ]
    
    def __str__(self):
        return f"Video for {self.portfolio_item.title}"
    
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.video_type == 'upload' and not self.video_file:
            raise ValidationError('Uploaded videos require a video file.')
        if self.video_type in ['youtube', 'vimeo'] and not self.video_url:
            raise ValidationError('External videos require a video URL.')

class Client(models.Model):
    CATEGORY_CHOICES = [
        ('all', 'All'),
        ('transportation', 'Transportation'),
        ('construction', 'Construction'),
        ('import_export', 'Import and Export'),
        ('industrial', 'Industrial'),
    ]

    name = models.CharField(max_length=200, db_index=True)  # Added index
    logo = models.ImageField(upload_to='clients/logos/')
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='all',
        db_index=True  # Added index
    )
    active = models.BooleanField(default=True, db_index=True)  # Added index

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['category', 'active']),
            models.Index(fields=['active', 'name']),
        ]

    def __str__(self):
        return self.name

class Testimonial(models.Model):
    client = models.ForeignKey(
        Client, 
        on_delete=models.CASCADE, 
        related_name='testimonials',
        db_index=True  # Added index
    )
    author_name = models.CharField(max_length=150, db_index=True)  # Added index
    position = models.CharField(max_length=150, blank=True, null=True)
    quote = models.TextField()
    display = models.BooleanField(default=True, db_index=True)  # Added index
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)  # Added index

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['display', 'created_at']),
            models.Index(fields=['client', 'display']),
        ]

    def __str__(self):
        return f"{self.author_name} - {self.client.name}"

class BasicWebsiteInfo(models.Model):
    phone = models.CharField(max_length=10)
    featured_news = models.CharField(max_length=150, null=True, blank=True)
    email = models.EmailField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    news = models.CharField(max_length=200, null=True, blank=True)

    def clean(self):
        if BasicWebsiteInfo.objects.exclude(id=self.id).exists():
            raise ValidationError("Only one Basic Website Info instance is allowed.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return "Website Basic Info"

class SocialLink(models.Model):
    PLATFORM_CHOICES = [
        ('facebook', 'Facebook'),
        ('twitter', 'Twitter (X)'),
        ('instagram', 'Instagram'),
        ('linkedin', 'LinkedIn'),
        ('youtube', 'YouTube'),
        ('tiktok', 'TikTok'),
        ('telegram', 'Telegram'),
        ('whatsapp', 'WhatsApp'),
        ('snapchat', 'Snapchat'),
        ('pinterest', 'Pinterest'),
        ('github', 'GitHub'),
        ('behance', 'Behance'),
        ('dribbble', 'Dribbble'),
    ]

    platform = models.CharField(max_length=50, choices=PLATFORM_CHOICES, db_index=True)  # Added index
    url = models.URLField()
    icon_class = models.CharField(max_length=50, blank=True)
    website_info = models.ForeignKey(
        BasicWebsiteInfo,
        on_delete=models.CASCADE,
        related_name='social_links',
        db_index=True  # Added index
    )

    class Meta:
        unique_together = ('platform', 'website_info')
        verbose_name = 'Social Link'
        verbose_name_plural = 'Social Links'
        ordering = ['platform']
        indexes = [
            models.Index(fields=['website_info', 'platform']),
        ]

    def save(self, *args, **kwargs):
        if not self.icon_class:
            # Simplified icon mapping
            icon_map = {
                'facebook': 'fab fa-facebook-f',
                'twitter': 'fab fa-twitter',
                'instagram': 'fab fa-instagram',
                'linkedin': 'fab fa-linkedin-in',
                'youtube': 'fab fa-youtube',
                'tiktok': 'fab fa-tiktok',
                'telegram': 'fab fa-telegram',
                'whatsapp': 'fab fa-whatsapp',
                'snapchat': 'fab fa-snapchat-ghost',
                'pinterest': 'fab fa-pinterest',
                'github': 'fab fa-github',
                'behance': 'fab fa-behance',
                'dribbble': 'fab fa-dribbble',
            }
            self.icon_class = icon_map.get(self.platform, 'fas fa-link')
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_platform_display()} - {self.url}"

class IndustrialPage(models.Model):
    """Model for the Industrial page content"""

    hero_title = models.CharField(max_length=200, default="Product Name", db_index=True)  # Added index
    hero_image = models.ImageField(
        upload_to='industrial/hero/',
        default='industrial/hero/car-bg.jpg'
    )
    hero_icon_text = models.CharField(max_length=10, default="X")

    motor = models.CharField(max_length=50, default='') 
    battery = models.TextField(default='')
    top_speed = models.CharField(max_length=50, default='')
    rangee = models.TextField(default='')

    is_active = models.BooleanField(default=True, db_index=True)  # Added index
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Industrial Page"
        verbose_name_plural = "Industrial Page"
        indexes = [
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return self.hero_title

class ImportExportProductCategory(models.Model):
    """Model for Import & Export product categories"""
    
    title = models.CharField(max_length=100, db_index=True)  # Added index
    description = models.TextField()
    image = models.ImageField(upload_to='products/')
    is_active = models.BooleanField(default=True, db_index=True)  # Added index
    order = models.PositiveIntegerField(default=0, db_index=True)  # Added index

    class Meta:
        ordering = ['order']
        verbose_name = "Import Export"
        verbose_name_plural = "Import Exports"
        indexes = [
            models.Index(fields=['is_active', 'order']),
            models.Index(fields=['order', 'is_active']),
        ]

    def __str__(self):
        return self.title
    



from django.db import models

class HeroMedia(models.Model):
    # Landing Page
    landing_background_image = models.ImageField(upload_to='hero_images/', blank=True, null=True)
    landing_background_video = models.FileField(upload_to='hero_videos/', blank=True, null=True)

    # Construction Page
    construction_background_image = models.ImageField(upload_to='hero_images/', blank=True, null=True)
    construction_background_video = models.FileField(upload_to='hero_videos/', blank=True, null=True)

    # Industrial Page
    industrial_background_image = models.ImageField(upload_to='hero_images/', blank=True, null=True)
    industrial_background_video = models.FileField(upload_to='hero_videos/', blank=True, null=True)

    # Import & Export Page
    import_export_background_image = models.ImageField(upload_to='hero_images/', blank=True, null=True)
    import_export_background_video = models.FileField(upload_to='hero_videos/', blank=True, null=True)

    # Transport Page
    transport_background_image = models.ImageField(upload_to='hero_images/', blank=True, null=True)
    transport_background_video = models.FileField(upload_to='hero_videos/', blank=True, null=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Hero Section Media (Global)"

    def save(self, *args, **kwargs):
        """Ensure only one instance exists."""
        if not self.pk and HeroMedia.objects.exists():
            raise ValueError("Only one HeroMedia instance is allowed.")
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Hero Media"
        verbose_name_plural = "Hero Media"




class Vehicle(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='vehicles/')
    order = models.PositiveIntegerField(default=0)

    # Optional: short tagline like “Premium mobility for leaders”
    tagline = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name


class VehicleFeature(models.Model):
    vehicle = models.ForeignKey(Vehicle, related_name="features", on_delete=models.CASCADE)
    feature_text = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.vehicle.name} - {self.feature_text}"
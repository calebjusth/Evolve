from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse
from ckeditor.fields import RichTextField

class BlogCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, db_index=True)  # Added db_index
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),  # Added index for name
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')
    

class BlogPost(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique_for_date='publish_date', db_index=True)  # Added db_index
    author = models.CharField(max_length=100)
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True, blank=True, db_index=True)  # Added db_index
    featured_image = models.ImageField(upload_to='blog/featured_images/', blank=True, null=True)
    content = RichTextField()
    excerpt = models.TextField(max_length=300, blank=True)
    publish_date = models.DateTimeField(default=timezone.now, db_index=True)  # Added db_index - crucial for ordering
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft', db_index=True)  # Added db_index
    views = models.PositiveIntegerField(default=0, db_index=True)  # Added db_index for popular posts
    tags = models.ManyToManyField('BlogTag', blank=True, related_name='blogposts')

    class Meta:
        ordering = ['-publish_date']
        indexes = [
            # Composite index for common query patterns
            models.Index(fields=['status', 'publish_date']),  # For published posts ordered by date
            models.Index(fields=['category', 'status', 'publish_date']),  # For category pages
            models.Index(fields=['author', 'publish_date']),  # For author archive pages
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:blog_post_detail', args=[
            self.publish_date.year,
            self.publish_date.month,
            self.publish_date.day,
            self.slug
        ])
    
    objects = models.Manager()              # The default manager
    published = PublishedManager() 


class BlogComment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments', db_index=True)  # Added db_index
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    comment = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True, db_index=True)  # Added db_index
    active = models.BooleanField(default=False, db_index=True)  # Added db_index for moderation

    class Meta:
        ordering = ['created_date']
        indexes = [
            models.Index(fields=['post', 'active', 'created_date']),  # For loading comments for a post
        ]

    def __str__(self):
        return f"Comment by {self.name} on {self.post.title}"


class BlogTag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=60, unique=True, db_index=True)  # Added db_index
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        indexes = [
            models.Index(fields=['name']),  # Added index for name
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog_tag_detail', args=[self.slug])